from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from prefeitura_rio.pipelines_templates.dump_url.flows import dump_url_flow
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters
from prefeitura_rio.pipelines_utils.state_handlers import (
    handler_initialize_sentry,
    handler_inject_bd_credentials,
)

from pipelines.constants import constants
from pipelines.geosislic.dump_url.schedules import gsheets_four_year_update_schedule

smdue_geosislic_gsheets_flow = deepcopy(dump_url_flow)
smdue_geosislic_gsheets_flow.state_handlers = [
    handler_inject_bd_credentials,
    handler_initialize_sentry,
]
smdue_geosislic_gsheets_flow.name = "SMDUE: GEOSISLIC - Ingerir CSV do Google Drive"
smdue_geosislic_gsheets_flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
smdue_geosislic_gsheets_flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[
        constants.RJ_SMDUE_AGENT_LABEL.value,
    ],
)

smdue_geosislic_gsheets_default_parameters = {
    "dataset_id": "geosislic",
}
smdue_geosislic_gsheets_flow = set_default_parameters(
    smdue_geosislic_gsheets_flow, default_parameters=smdue_geosislic_gsheets_default_parameters
)

smdue_geosislic_gsheets_flow.schedule = gsheets_four_year_update_schedule
