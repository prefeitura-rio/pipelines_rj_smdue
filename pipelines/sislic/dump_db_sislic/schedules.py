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
                codOrgaoSMU,
                codRa
            FROM SMU_PRD.dbo.tbLogra_Bairros
            """,
    },
    "tramite_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codTramite,
                matricCadastrador,
                codDocumento,
                dtCadastro,
                dtSaida,
                vfDestinoOrgao,
                codDestino,
                matricOrigem,
                matricDestino,
                codOrigem,
                status
            FROM SMU_PRD.dbo.tbPTI_Tramites
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
                descDespacho
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
                DS_AREA_PROTECAO_CULTURAL
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
                ID_Endereco,
                Num_lic,
                cLogra,
                Tipo,
                Nobreza,
                Preposicao,
                NomeLogra,
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
                Num_Edif,
                Num_lic,
                Cod_Tp_edif,
                cod_Compl_Tp_Edif,
                cod_Compl_Tp_Edif2,
                Compl_Livre,
                area_edif,
                area_acresc,
                area_reduzida,
                area_util,
                embasamento,
                RecebeNumeracao,
                ContaEdificacao,
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
                id_edif,
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
                Pavimento,
                Tot_pav,
                tot_vagasCobertas,
                Tot_VagasDescobertas
            FROM SMU_PRD.dbo.tbLIC_PavimentosLicencas
            """,
    },
    "subdivisao_edificacao_obra": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_SubDivisao,
                num_lic,
                id_edif,
                descSubDivisao
            FROM SMU_PRD.dbo.tbLIC_SubDivisoesEdificacao
            """,
    },
    "unidade_edificacao_obra": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_Unid,
                num_lic,
                id_edif,
                id_SubDivisao,
                cod_unidade,
                ComplTipo_Unid,
                quant_unid,
                Num_recebida,
                area_unid
            FROM SMU_PRD.dbo.tbLIC_UnidadesLicencas
            """,
    },
    "darm_licenca_alvara": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Num_Darm,
                cod_Classe,
                cod_Tipo_Lic,
                cod_Lic,
                cod_Compl_Lic,
                compl_Livre,
                Valor,
                Formula
            FROM SMU_PRD.dbo.tbLIC_LicencasDARMs
            """,
    },
    "darm_alvara": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                num_Darm,
                DARM,
                Num_Lic,
                CNPJ_CPF,
                Cod_Receita,
                Dt_Emissao,
                Dt_Venc,
                Dt_Pagamento,
                Competencia,
                Mora,
                Multa,
                Valor_Darm_Inicial,
                ValorDarm,
                Cancelado,
                Dt_Calculo,
                InscIPTU,
                Avulso
            FROM SMU_PRD.dbo.tbLIC_DARMS
            """,
    },
    "licenca_alvara": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_Lic,
                num_lic,
                id_edif,
                cod_classe,
                cod_tipo_lic,
                cod_lic,
                cod_compl_lic,
                Compl_Livre,
                Dec9218,
                OutroDec,
                ObrasConcluidas
            FROM SMU_PRD.dbo.tbLIC_LicencasEdificacoes
            """,
    },
    "loteamento_alvara": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                num_lic,
                LotesVinculados,
                ComprLograProjetados,
                TotalLotesPrimitivosRemembramento,
                TotalLotesRemembrados,
                TotalLotesPrimitivosDesmembramento,
                TotalLotesDesmembrados,
                TotalLotesPrimitivosReDesmembramento,
                TotalLotesReDesmembrados,
                TotalAreasPrivativasPrimitivas,
                TotalAreasPrivativasResultantes
            FROM SMU_PRD.dbo.tbLIC_ComplementacaoLicencaLoteamento
            """,
    },
    "licenca_substituida": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                num_Lic_Substituida,
                num_lic_Nova,
                DtSubstituicao,
                Motivo,
                Retificacao,
                RetificacaoTotal,
                RecalculoDarm_Liberado
            FROM SMU_PRD.dbo.tbLIC_LicencasSubstituidas
            """,
    },
    "licenca_loteamento": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_Lote,
                num_lic,
                Quantidade,
                Categoria,
                TpLote
            FROM SMU_PRD.dbo.tbLIC_IdentificacaoLotesLicenca
            """,
    },
    "restricao_alvara": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Id_Rest,
                num_lic,
                cod_Restricao,
                Compl_Restricao,
                Outra_restricao,
                Data_Baixa,
                BAIXA_EXOFFICIO
            FROM SMU_PRD.dbo.tbLIC_RestricoesLicencas
            """,
    },
    "restricao_fase": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Cod_restricao,
                Cod_fase,
                desc_restricao,
                Tipo_Compl,
                Compl,
                ATIVO
            FROM SMU_PRD.dbo.tbLic_restricoes
            """,
    },
    "fase_obra": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Cod_Fase,
                Abrev_Fase,
                OrdemImp
            FROM SMU_PRD.dbo.tbLic_FasesObras
            """,
    },
    "tipo_edificacao": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Cod_TpEdificacao,
                Desc_TpEdificacao
            FROM SMU_PRD.dbo.tbLic_TiposEdificacoes
            """,
    },
    "compl_1_tipo_edificacao": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Cod_TpEdificacao,
                Cod_Compl_TpEdificacao,
                Compl_TpEdificacao
            FROM SMU_PRD.dbo.tbLic_ComplTpEdificacoes1
            """,
    },
    "compl_2_tipo_edificacao": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                cod_Edif,
                cod_compl_TpEdificacao,
                cod_compl_tpEdificacao2,
                Compl2
            FROM SMU_PRD.dbo.tbLic_ComplTpEdificacoes2
            """,
    },
    "tipo_licenca_acao_requerente": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                COD_LIC,
                DESCR_LIC,
                TAB_AUX_CATEGORIA,
                TAB_AUX_AREA,
                GRATIS,
                COMPL,
                Compl_Obrigatorio
            FROM SMU_PRD.dbo.tbLic_DescricoesLicencas
            """,
    },
    "compl_tipo_licenca_acao_requerente": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                COD_LIC,
                COD_COMPL_LIC,
                COMPL,
                GRATIS
            FROM SMU_PRD.dbo.tbLic_ComplementosTpLicencas
            """,
    },
    "tipo_licenca_acao_prefeitura_1": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                COD_TIPO_LIC,
                DESCR_TIPO_LIC
            FROM SMU_PRD.dbo.tbLic_TiposLicencas
            """,
    },
    "tipo_licenca_acao_prefeitura_2": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                cod_classe,
                descr_classe
            FROM SMU_PRD.dbo.tbLIC_ClassesLicencas
            """,
    },
    "tipo_unidade": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Desc_Unidade,
                Desc_unidade_Plural
            FROM SMU_PRD.dbo.tbLIC_Unidades
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
