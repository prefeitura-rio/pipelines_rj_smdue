# -*- coding: utf-8 -*-
"""
Database dumping flows for segovi project (SISLIC)
"""

from copy import deepcopy

from prefect.run_configs import KubernetesRun
from prefect.storage import GCS

from prefeitura_rio.pipelines_templates.dump_db.flows import flow as dump_sql_flow
from prefeitura_rio.pipelines_utils.prefect import set_default_parameters
from prefeitura_rio.pipelines_utils.state_handlers import (
    handler_initialize_sentry,
    handler_inject_bd_credentials,
)

from pipelines.constants import constants
from pipelines.sislic.dump_db_sislic.schedules import (
    update_schedule,
)

dump_sislic_flow = deepcopy(dump_sql_flow)
dump_sislic_flow.name = "SMDUE: SISLIC - Ingerir tabelas de banco SQL"
dump_sislic_flow.state_handlers = [handler_inject_bd_credentials, handler_initialize_sentry]
dump_sislic_flow.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
dump_sislic_flow.run_config = KubernetesRun(
    image=constants.DOCKER_IMAGE.value,
    labels=[
        constants.RJ_SMDUE_AGENT_LABEL.value,
    ],
)

sislic_default_parameters = {
    "db_database": "SMU_PRD",
    "db_host": "10.2.221.101",
    "db_port": "1433",
    "db_type": "sql_server",
    "infisical_secret_path": "/db_sislic",
    "dataset_id": "adm_licenca_urbanismo",
}
dump_sislic_flow = set_default_parameters(
    dump_sislic_flow, default_parameters=sislic_default_parameters
)

dump_sislic_flow.schedule = update_schedule
