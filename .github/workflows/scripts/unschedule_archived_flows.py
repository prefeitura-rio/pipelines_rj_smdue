# -*- coding: utf-8 -*-
"""
UNSCHEDULE ARCHIVED FLOWS
----------------------------
This script is used to unschedule archived flows with scheduled runs in Prefect.
- Everytime a flow is registered in Prefect, a new version is created and the old versions archived.
- Sometimes, the old versions have remaining scheduled runs, which can cause issues. We call then GHOST RUNS.
- This script queries the Prefect API for archived flows with scheduled runs and unschedules them.
- Adapted from SMTR's flow called Janitor
"""
import argparse
from datetime import datetime
import time

from loguru import logger

try:
    from prefect import Client
    from prefect.utilities.graphql import with_args
except ImportError:
    from prefeitura_rio.utils import base_assert_dependencies

    base_assert_dependencies(["basedosdados", "prefect"], extras=["pipelines"])


def log(message, level="debug"):
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)


def get_project_id(client: Client, project: str) -> str:
    """
    (Adapted from Prefect original code.)

    Get a project id given a project name.

    Args:
        - project (str): the project name

    Returns:
        - str: the project id
    """
    resp = client.graphql(
        {"query": {with_args("project", {"where": {"name": {"_eq": project}}}): {"id"}}}
    )
    if resp.data.project:
        return resp.data.project[0].id
    raise Exception(f"Project {project!r} does not exist")  # noqa


def query_non_archived_flows(prefect_client, environment="staging"):
    """
    Queries the non-archived flows from the Prefect API for a given environment.

    Args:
        environment (str, optional): The environment to query the flows from.

    Returns:
        list: A list of unique non-archived flows in the format [(name, version)].

    Raises:
        Exception: If there is an error in the GraphQL request or response.
    """
    project_name = "production" if environment == "prod" else environment
    query = """
        query ($offset: Int, $project_name: String){
            flow(
                where: {
                    archived: {_eq: false},
                    project: {name:{_eq:$project_name}}
                }
                offset: $offset
            ){
                name
                version
            }
        }
    """

    # Request data from Prefect API
    request_response = prefect_client.graphql(
        query=query, variables={"offset": 0, "project_name": project_name}
    )
    data = request_response["data"]

    active_flows = [(flow["name"], flow["version"]) for flow in data["flow"]]
    log(f"Number of Non Archived Flows: {len(active_flows)}")

    unique_non_archived_flows = list(set(active_flows))
    log(f"Number of Unique Non Archived Flows: {len(unique_non_archived_flows)}")

    lines = [f"- {flow['name']}@v{flow['version']}" for flow in data["flow"]]
    message = f"Non Archived Flows in Project {project_name}:\n" + "\n".join(lines)
    log(message)

    return unique_non_archived_flows


def query_archived_flow_versions_with_runs(flow_data, prefect_client, environment="staging"):
    """
    Queries for archived flow versions with scheduled runs.

    Args:
        flow_data (tuple): A tuple containing the flow name and the last version.
        environment (str, optional): The environment to query the flows in.

    Returns:
        list: A list of dictionaries representing the archived flow versions with scheduled runs.
            Each dictionary contains the following keys:
                - id (str): The ID of the flow.
                - name (str): The name of the flow.
                - version (int): The version of the flow.
                - invalid_runs_count (int): The number of invalid runs for the flow.
    """

    project_name = "production" if environment == "prod" else environment
    flow_name, last_version = flow_data

    log(f"Querying for archived flow runs of {flow_name} < v{last_version} in {project_name}.")
    now = datetime.now().isoformat()
    query = """
        query($flow_name: String, $last_version: Int, $now: timestamptz!, $offset: Int, $project_name: String){ # noqa
            flow(
                where:{
                    name: {_eq:$flow_name},
                    version: {_lt:$last_version}
                    project: {name:{_eq:$project_name}}
                }
                offset: $offset
                order_by: {version:desc}
            ){
                id
                name
                version
                flow_runs(
                    where:{
                        scheduled_start_time: {_gte: $now},
                        state: {_nin: ["Cancelled"]}
                    }
                    order_by: {version:desc}
                ){
                    id
                    scheduled_start_time
                }
            }
        }
    """

    # Request data from Prefect API
    request_response = prefect_client.graphql(
        query=query,
        variables={
            "flow_name": flow_name,
            "last_version": last_version,
            "now": now,
            "offset": 0,
            "project_name": project_name,
        },
    )

    data = request_response["data"]

    flow_versions_to_cancel = []
    for flow in data["flow"]:
        flow_runs = flow["flow_runs"]

        # Se não houver flow_runs futuras, não é necessário cancelar
        if len(flow_runs) == 0:
            continue

        flow_versions_to_cancel.append(
            {
                "id": flow["id"],
                "name": flow["name"],
                "version": flow["version"],
                "invalid_runs_count": len(flow_runs),
            }
        )

    if len(flow_versions_to_cancel) == 0:
        log(f"No archived flows with scheduled runs found for {flow_name} < v{last_version}.")
        return []

    lines = [
        f"- {flow['name']} @ v{flow['version']} ({flow['id']}) has {flow['invalid_runs_count']} invalid runs"  # noqa
        for flow in flow_versions_to_cancel
    ]
    message = f"Archived Flows with Scheduled Runs in Project {project_name}:\n" + "\n".join(lines)
    log(message)

    return flow_versions_to_cancel


def archive_flow_versions(flow_versions_to_archive: list, prefect_client: Client) -> None:
    """
    Archive flow versions from the API.
    """
    query = """
        mutation($flow_id: UUID!) {
            archive_flow (
                input: {
                    flow_id: $flow_id
                }
            ) {
                success
            }
        }
    """
    reports = []
    for flow in flow_versions_to_archive:
        response = prefect_client.graphql(query=query, variables=dict(flow_id=flow["id"]))

        flow_title = f"{flow['name']} @ v{flow['version']}"
        flow_url = f"https://pipelines.dados.rio/flow/{flow['id']}"
        report = f"- [{flow_title}]({flow_url}) arquivado com status=`{response}`"

        reports.append(report)

    reports = sorted(reports)
    log("\n".join(reports))


def main():

    time.sleep(60)
    parser = argparse.ArgumentParser(description="Process a project name.")
    parser.add_argument("--project", type=str, required=True, help="Name of the project")
    parser.add_argument("--environment", type=str, required=True, help="Environment the project")

    args = parser.parse_args()

    prefect_client = Client()

    active_flows = query_non_archived_flows(prefect_client, args.environment)

    results = []
    for flow in active_flows:
        flows_to_archive = query_archived_flow_versions_with_runs(
            flow, prefect_client, args.environment
        )
        results.extend(flows_to_archive)

    log(f"Total archived flows with scheduled runs: {len(results)}")

    log("Archiving flows...")
    archive_flow_versions(results, prefect_client)

    log("Done!")


if __name__ == "__main__":
    main()
