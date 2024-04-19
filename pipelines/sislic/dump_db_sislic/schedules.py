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
    # "cronograma_financeiro": {
    #     "materialize_after_dump": True,
    #     "materialization_mode": "prod",
    #     "dump_mode": "overwrite",
    #     "execute_query": """
    #         Select
    #             DISTINCT
    #                 CD_OBRA,
    #                 ETAPA,
    #                 DT_INICIO_ETAPA,
    #                 DT_FIM_ETAPA,
    #                 PC_PERCENTUAL,
    #                 VL_ESTIMADO
    #         from dbo.fuSEGOVI_Cronograma_Financeiro()
    #         """,
    # },
    # "localizacao": {
    #     "materialize_after_dump": True,
    #     "materialization_mode": "prod",
    #     "dump_mode": "overwrite",
    #     "execute_query": """
    #         Select
    #             CD_OBRA,
    #             ENDERECO,
    #             NM_BAIRRO,
    #             NM_RA,
    #             NM_AP
    #         from dbo.fuSEGOVI_Localizacoes_obra()
    #         """,
    # },
    # "cronograma_alteracao": {
    #     "materialize_after_dump": True,
    #     "materialization_mode": "prod",
    #     "dump_mode": "overwrite",
    #     "execute_query": """
    #         Select
    #             DISTINCT
    #                 CD_OBRA,
    #                 NR_PROCESSO,
    #                 TP_ALTERACAO,
    #                 DT_PUBL_DO,
    #                 CD_ETAPA,
    #                 NR_PRAZO,
    #                 DT_VALIDADE,
    #                 DS_OBSERVACAO
    #         from dbo.fuSEGOVI_Alteração_de_Cronograma()
    #         """,
    # },
    # "programa_fonte": {
    #     "materialize_after_dump": True,
    #     "materialization_mode": "prod",
    #     "dump_mode": "overwrite",
    #     "execute_query": """
    #         Select
    #             DISTINCT
    #                 CD_OBRA,
    #                 CD_PRG_TRAB,
    #                 PROGRAMA_TRABALHO,
    #                 CD_FONTE_RECURSO,
    #                 FONTE_RECURSO,
    #                 CD_NATUREZA_DSP,
    #                 NATUREZA_DESPESA
    #         from dbo.fuSEGOVI_Programa_Fonte()
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
