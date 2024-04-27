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
    "requerente_processo_documento": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codPessoa,
                nomPessoa,
                telPessoa,
                EmailPessoa,
                CPF_CNPJ,
                vfFisica,
                identidade,
                emissor,
                cep,
                dtCadastro,
                matricCadastrador,
                Bairro,
                UF,
                codLogra,
                descLogra,
                numero,
                compend,
                municipio,
                inscmunicipal
            FROM SMU_PRD.dbo.tbPTI_Pessoas
            """,
    },
    "requerente_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codDocumento,
                codPessoa,
                vfTitular,
                matricCadastrador,
                dtCadastro
            FROM SMU_PRD.dbo.tbPTI_ProcessosRequerentes
            """,
    },
    "endereco_obra_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codDocumento,
                codEndereco,
                vfPrincipal,
                matricCadastrador,
                dtCadastro
            FROM SMU_PRD.dbo.tbPTI_EnderecosProcessos
            """,
    },
    "orgao_tramitacao_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codOrgaoSMU,
                codOrgaoSici,
                sigla,
                nomOrgao,
                cancelado,
                COD_Secretaria,
                permiteAgendamento
            FROM SMU_PRD.dbo.tbLogra_Orgaos
            """,
    },
    "classificacao_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_CLASSIFICACAO_PROCESSO, 
                DS_CLASSIFICACAO_PROCESSO
            FROM SMU_PRD.dbo.tbPTI_ClassificacaoProcesso
            """,
    },
    "processo_apenso": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codDocumentoPrincipal,
                codDocumentoApenso,
                MatricCadastrador
            FROM SMU_PRD.dbo.tbPTI_Apensos
            """,
    },
    "tipo_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_TIPO_PROCESSO,
                DS_TIPO_PROCESSO
            FROM SMU_PRD.dbo.tbPTI_TiposProcessos 
            """,
    },
    "orgao_origem_classificacao": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_ORIGEM_CLASSIFICACAO_PROCESSO,
                DS_ORIGEM_CLASSIFICACAO_PROCESSO
            FROM SMU_PRD.dbo.tbPTI_OrigemClassificacaoProcesso 
            """,
    },
    "area_protecao_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_AREA_GRAU,
                ID_AREA_PROTECAO_CULTURAL,
                ID_GRAU_PROTECAO,
                ANTERIOR_1938,
                SITIO_RIO_PATRIMONIO_MUNDIAL
            FROM SMU_PRD.dbo.tbPTI_IRPH_Complemento_Area_Grau_Protecao
            """,
    },
    "processo_irph": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_IRPH_DOCTO,
                CODDOCUMENTO,
                DESCRICAO
            FROM SMU_PRD.dbo.tbPTI_IRPH_Complemento_Processo
            """,
    },
    "preo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_PREO,
                CODDOCUMENTO,
                NOME_PREO,
                CPF_PREO,
                EMAIL_PREO,
                TELEFONE_PREO,
                TIPO_REGISTRO_PREO,
                NUMERO_REGISTRO_PREO,
                TIPO_CONSELHO_PREO,
                NUMERO_CONSELHO_PREO,
                ID_PROFISSAO
            FROM SMU_PRD.dbo.tbPTI_PREO 
            """,
    },
    "prpa": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_PRPA,
                CODDOCUMENTO,
                NOME_PRPA,
                CPF_PRPA,
                EMAIL_PRPA,
                TELEFONE_PRPA,
                TIPO_REGISTRO_PRPA,
                NUMERO_REGISTRO_PRPA,
                TIPO_CONSELHO_PRPA,
                NUMERO_CONSELHO_PRPA,
                ID_PROFISSAO
            FROM SMU_PRD.dbo.tbPTI_PRPA
            """,
    },
    "profissao_preo_prpa": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_PROFISSAO,
                DS_PROFISSAO
            FROM SMU_PRD.dbo.tbPTI_Profissao
            """,
    },
    "despacho": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codTramite,
                codParecer,
                descDespacho,
                vfCumprido
            FROM SMU_PRD.dbo.tbPTI_Despachos
            """,
    },
    "tipo_parecer_tramite": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codParecer,
                descParecer,
                vfGeraPublicacao,
                descClassificacao,
                PUBLICACAO_FRENTE_DO
            FROM SMU_PRD.dbo.tbPTI_TiposPareceres
            """,
    },
    "linha_publicacao_tramite": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codLinha,
                codTramite,
                codPublicacao,
                dtExpediente,
                codOrgao,
                descTipoDespacho,
                numero,
                texto,
                texto_final,
                requerente,
                dtCadastro,
                matricLiberador,
                dtliberacao
            FROM SMU_PRD.dbo.tbPTI_Linha
            """,
    },
    "endereco_produto_pedido": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                codEndereco,
                codLogra,
                numPorta,
                complPorta,
                codBairro,
                numPAL,
                numQuadra,
                numLote,
                vfMunicipal,
                UF,
                numPAA,
                dtCadastro,
                matricCadastrador,
                CEP,
                InscricaoIMOVEL,
                ID_TpInscricaoIMOVEL
            FROM SMU_PRD.dbo.tbPTI_Enderecos
            """,
    },
    "publicacao_domrj": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codPublicacao,
                dtEnvio,
                dtPublicacao,
                dtPrevista
            FROM SMU_PRD.dbo.tbPTI_Publicacao
            """,
    },
    "area_protecao_cultural": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_AREA_PROTECAO_CULTURAL,
                DS_AREA_PROTECAO_CULTURAL,
                OPCAO_GRAU_PROTECAO,
                ANTERIOR_1938_ESTADO_DEFAULT,
                SITIO_RIO_PATRIMONIO_MUNDIAL_ESTADO_DEFUALT,
                ANTERIOR_1938_AUTOMATICO,
                SITIO_RIO_AUTOMATICO
            FROM SMU_PRD.dbo.tbPTI_IRPH_Area_Protecao_Cultural tpiapc
            """,
    },
    "grau_protecao_area": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_GRAU_PROTECAO,
                DS_GRAU_PROTECAO
            FROM SMU_PRD.dbo.tbPTI_IRPH_Grau_Protecao
            """,
    },
    "alvara_obra_privada": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                licenca,
                num_proc,
                cod_dlf,
                Dt_emissao,
                Dt_Inicio_Validade,
                Prazo,
                dt_Venc,
                Dt_alvara,
                Num_darm_pg,
                Vl_Lic,
                Requerente,
                CNPJ_CPF,
                clogra,
                tipo,
                nobreza,
                preposicao,
                nomelogra,
                num,
                complemento,
                paa,
                pal,
                PLT,
                quadra,
                lote,
                cb,
                zona,
                subzona,
                cep,
                bsmp,
                num_suple,
                InscricaoIMOVEL,
                ID_TpInscricaoIMOVEL,
                Uso_atividade,
                Implantacao,
                tot_edif,
                area_constr,
                area_acrescida,
                area_reduzida,
                area_util,
                AREA_TOTAL_EDIFICADA,
                AREA_EXISTENTE_DECLARADA_RESPONSAVEL,
                AreaTotal_Loteamento,
                MetrosLineares_ObrasUrbanizacao,
                VagasExternasDescobertas,
                VagasExternasCobertas,
                VagasPavimentos,
                nome_preo,
                crea_preo,
                RRT_ART_PREO,
                Nome_PRPA,
                Crea_PRPA,
                RRT_ART_PRPA,
                Grupamento,
                Tot_etapas,
                Tot_edif_etapa,
                area_tot_etapa,
                Lic_concedida,
                Edif_Pav,
                ConcedeNumeracao,
                NumConcedida,
                OBS,
                cancelado,
                OrgaoCentral,
                CODORGAO_ESPECIAL,
                Licenca_Loteamento,
                LicencaAvulsa,
                LoteamentoNovoModelo,
                AprovacaoParcelamento,
                Totalunidades,
                LicOnLine_ID_Requerimento
            FROM SMU_PRD.dbo.tbLIC_Licencas
            """,
    },
    "endereco_obra_alvara": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT 
                ID_Endereco ,
                Num_lic,
                cLogra,
                Tipo ,
                Nobreza ,
                Preposicao ,
                NomeLogra ,
                Num
            FROM SMU_PRD.dbo.tbLIC_EnderecosLicenca
            """,
    },
    "edificacao_obra_licenca": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_edif,
                Num_Edif ,
                Num_lic,
                Cod_Tp_edif ,
                cod_Compl_Tp_Edif ,
                cod_Compl_Tp_Edif2 ,
                Compl_Livre,
                area_edif ,
                area_acresc ,
                area_reduzida ,
                area_util ,
                embasamento ,
                RecebeNumeracao ,
                ContaEdificacao ,
                Qtd_Edif 
            FROM SMU_PRD.dbo.tbLIC_EdificacoesLicencas
            """,
    },
    "endereco_edificacao": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                id_edif ,
                ID_Endereco
            FROM SMU_PRD.dbo.tbLIC_EnderecosEdificacao
            """,
    },
    "pavimento_edificacao_obra": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_Pav,
                Num_lic,
                Id_Edif,
                Pavimento ,
                Tot_pav ,
                tot_vagasCobertas,
                Tot_VagasDescobertas 
            FROM SMU_PRD.dbo.tbLIC_PavimentosLicencas
            """,
    },
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
