# -*- coding: utf-8 -*-
# flake8: noqa: E501

"""
Schedules for the SISLIC dump pipeline
"""

from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
    },
    "despacho": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codTramite,
                codParecer,
                REPLACE(REPLACE(CAST(descDespacho AS VARCHAR(MAX)), CHAR(13), ' '), CHAR(10), ' ') AS descDespacho
            FROM SMU_PRD.dbo.tbPTI_Despachos
            """,
        "biglake_table": True,
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
        "biglake_table": True,
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
                REPLACE(REPLACE(CAST(texto AS VARCHAR(MAX)), CHAR(13), ' '), CHAR(10), ' ') AS texto,
                REPLACE(REPLACE(CAST(texto_final AS VARCHAR(MAX)), CHAR(13), ' '), CHAR(10), ' ') AS texto_final,
                requerente,
                dtCadastro,
                matricLiberador,
                dtliberacao
            FROM SMU_PRD.dbo.tbPTI_Linha
            """,
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
    },
    "alvara_obra_privada": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                num_lic,
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
                mat_func,
                cancelado,
                licgratis,
                OrgaoCentral,
                CODORGAO_ESPECIAL,
                OrdemEmissao,
                Licenca_Loteamento,
                LicencaAvulsa,
                LoteamentoNovoModelo,
                AprovacaoParcelamento,
                Totalunidades,
                LicOnLine_ID_Requerimento
            FROM SMU_PRD.dbo.tbLIC_Licencas
            """,
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
                REPLACE(REPLACE(CAST(Outra_restricao AS VARCHAR(MAX)), CHAR(13), ' '), CHAR(10), ' ') AS Outra_restricao,
                Data_Baixa,
                BAIXA_EXOFFICIO
            FROM SMU_PRD.dbo.tbLIC_RestricoesLicencas
            """,
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
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
        "biglake_table": True,
    },
    "tipo_licenca_acao_prefeitura_2": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                COD_TIPO_LIC,
                DESCR_TIPO_LIC
            FROM SMU_PRD.dbo.tbLic_TiposLicencas
            """,
        "biglake_table": True,
    },
    "tipo_licenca_acao_prefeitura_1": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                cod_classe,
                descr_classe
            FROM SMU_PRD.dbo.tbLIC_ClassesLicencas
            """,
        "biglake_table": True,
    },
    "tipo_licenca_acao_prefeitura_4": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                cod_lic,
                cod_compl_lic,
                compl
            FROM SMU_PRD.dbo.tbLic_ComplementosTpLicencas
            """,
        "biglake_table": True,
    },
    "tipo_unidade": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                Cod_Unidade,
                Desc_Unidade,
                Desc_unidade_Plural
            FROM SMU_PRD.dbo.tbLIC_Unidades
            """,
        "biglake_table": True,
    },
    "certidao_habite_se": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                 Num_Hab
                ,Num_Proc
                ,Num_Lic
                ,Habite_se
                ,Cod_DLF
                ,Dt_Emissao
                ,Dt_Certidao
                ,Matricula_RGI
                ,Nr_Oficio_RGI
                ,Pal
                ,DescricaoLote
                ,Numeracao_Habitavel
                ,Mat_Tec_Resp
                ,Cancelado
                ,Habite_se_Total
                ,OBS
            FROM SMU_PRD.dbo.tbLIC_Habite_se
            """,
        "biglake_table": True,
    },
    "tipo_inscricao_imovel": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                ID_tpInscricaoImovel,
                TpInscricaoImovel
            FROM SMU_PRD.dbo.tbPTI_TiposInscricaoImovel
            """,
        "biglake_table": True,
    },
    "regiao_administrativa": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                codRA
                ,nomRA
                ,codAP
            FROM SMU_PRD.dbo.tbLogra_Ras
            """,
        "biglake_table": True,
    },
    "orgao_licenciamento": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
                CodOrgao
                ,CodOrgaoSigma
                ,Ativo
            FROM dbo.tbLIC_Orgaos
            """,
        "biglake_table": True,
    },
    "unidade_habite_se": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT ID
                ,Num_Hab
                ,Id_edif
                ,Quant_Edif
                ,Cod_Unidade
                ,Quant_Unidade
                ,Area
            FROM SMU_PRD.dbo.tbLIC_UnidadesHabite_se
            """,
        "biglake_table": True,
    },
    "certidao_aceitacao": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT Num_Aceitacao
                ,Num_Proc
                ,Num_Lic
                ,Aceitacao
                ,Cod_DLF
                ,Dt_Emissao
                ,Dt_Certidao
                ,Matricula_RGI
                ,Nr_Oficio_RGI
                ,PAL
                ,DescricaoLote
                ,Mat_Tec_Resp
                ,Cancelado
                ,Obs
            FROM SMU_PRD.dbo.tbLIC_Aceitacoes
            """,
        "biglake_table": True,
    },
    "georeferencia_endereco_obra_processo": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
            id_processo,
            id_processo_sislic,
            nu_processo,
            cd_logradouro,
            nu_porta,
            nu_pal,
            id_bairro_sislic,
            id_ra_sislic,
            no_bairro,
            shape
            FROM SMU_PRD.dbo.tbGEOSISLIC_processo
            """,
        "biglake_table": True,
    },
    "licenca_transferida": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
            SELECT
            num_lic_Origem,
            num_lic_Destino,
            DtTransferencia,
            Mat_Func,
            Nome_Func,
            Cargo_Func,
            MAQUINA_UTILIZADA,
            CODORGAOSIGMA_ORIGEM,
            CODORGAOSIGMA_DESTINO
            FROM SMU_PRD.dbo.tbLIC_LicencasTransferidasCLU_CRU

            """,
        "biglake_table": True,
    },
    "registro_cancelamento_produto": {
        "materialize_after_dump": True,
        "materialization_mode": "prod",
        "dump_mode": "overwrite",
        "execute_query": """
           SELECT
           cod_dlf,
           tipo,
           Nr_documento,
           dt_cancelamento,
           mat_func,
           nome_func,
           cargo_func,
           motivo,
           complmotivo,
           responsavel,
           outroresp,
           dt_autorizacao,
           MAQUINA_UTILIZADA

            FROM SMU_PRD.dbo.tbLIC_DocCancelados
            """,
        "biglake_table": True,
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
    runs_interval_minutes=5,
)

update_schedule = Schedule(clocks=untuple(sislic_clocks))
