# -*- coding: utf-8 -*-
"""
Schedules for the database dump pipeline
"""

from datetime import timedelta, datetime

from prefect.schedules import Schedule
import pytz

from prefeitura_rio.pipelines_utils.io import untuple_clocks as untuple
from prefeitura_rio.pipelines_utils.prefect import generate_dump_db_schedules

from pipelines.constants import constants

sislic_queries = {
    "documento": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codDocumento,
                numDocumento,
                codOrgao,
                codTipoDocumento,
                MatricCadastrador,
                dtAbertura,
                dtCadastroSistema,
                codAssunto,
                codDocumentoOrigem,
                descStatus,
                ID_CLASSIFICACAO_PROCESSO,
                ID_ORIGEM_CLASSIFICACAO_PROCESSO,
                ID_TIPO_PROCESSO,
                ANO_REQUERIMENTO,
                NUMERO_REQUERIMENTO
            FROM SMU_PRD.dbo.tbPTI_Documentos
            """,
    },
    "tipo_documento": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codTipoDocumento,
                descTipoDocumento
            FROM SMU_PRD.dbo.tbPTI_TiposDocumentos
            """,
    },
    "assunto_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codAssuntoN1,
                codAssuntoN2,
                codAssuntoN3,
                codAssunto,
                Status,
                codAssunto_ReqOnLine,
                Exige_Endereco,
                Exige_ProcessoConstrucao,
                Exige_CPF_CNPJ_Requerente,
                AssuntoProcessoRio
            FROM SMU_PRD.dbo.tbPTI_Assunto
            """,
    },
    "assunto_nivel_1": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                descNivel1,
                codAssuntoN1
            FROM SMU_PRD.dbo.tbPTI_AssuntosNivel1
            """,
    },
    "assunto_nivel_2": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                descNivel2,
                codAssuntoN2
            FROM SMU_PRD.dbo.tbPTI_AssuntosNivel2
            """,
    },
    "assunto_nivel_3": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                descNivel3,
                codAssuntoN3
            FROM SMU_PRD.dbo.tbPTI_AssuntosNivel3
            """,
    },
    "logradouro": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codLogra,
                codLograSMF,
                codTipoLogra,
                codNobreza,
                descPrepo,
                nomLogra
            FROM SMU_PRD.dbo.tbLogra_Logradouros
            """,
    },
    "bairro_logradouro": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codLogra,
                codBairro
            FROM SMU_PRD.dbo.tbLogra_LograBairros
            """,
    },
    "bairro": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codBairro,
                nomBairro,
                codOrgaoSMU
            FROM SMU_PRD.dbo.tbLogra_Bairros
            """,
    },
    "tramite_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codLogra,
                codLograSMF,
                codTipoLogra,
                codNobreza,
                descPrepo,
                nomLogra
            FROM SMU_PRD.dbo.tbLogra_Logradouros
            """,
    },
    # "lo": {
    #     "materialize_after_dump": True,
    #     "materialization_mode": "prod",
    #     "dump_mode": "overwrite",
    #     "execute_query": """
    #         SELECT
    #             codLogra,
    #             codLograSMF,
    #             codTipoLogra,
    #             codNobreza,
    #             descPrepo,
    #             nomLogra
    #         FROM SMU_PRD.dbo.tbLogra_Logradouros
    #         """,
    # },
    # "lo": {
    #     "materialize_after_dump": True,
    #     "materialization_mode": "prod",
    #     "dump_mode": "overwrite",
    #     "execute_query": """
    #         SELECT
    #             codLogra,
    #             codLograSMF,
    #             codTipoLogra,
    #             codNobreza,
    #             descPrepo,
    #             nomLogra
    #         FROM SMU_PRD.dbo.tbLogra_Logradouros
    #         """,
    # },
}

sislic_clocks = generate_dump_db_schedules(
    interval=timedelta(days=1),
    start_date=datetime(2022, 12, 19, 1, 0, tzinfo=pytz.timezone("America/Sao_Paulo")),
    labels=[
        constants.RJ_SMDUE_AGENT_LABEL.value,
    ],
    db_database="SMU_PRD",
    db_host="10.2.221.101",
    db_port="1433",
    db_type="sql_server",
    dataset_id="adm_licenca_urbanismo",
    infisical_secret_path="/db_sislic",
    table_parameters=sislic_queries,
)

update_schedule = Schedule(clocks=untuple(sislic_clocks))
