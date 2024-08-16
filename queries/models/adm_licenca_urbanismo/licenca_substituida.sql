SELECT
num_Lic_Substituida  AS Id_Licenciamento_Substituido ,
num_lic_Nova  AS Id_Licenciamento_Novo ,
CAST(DtSubstituicao AS DATETIME)  AS Data_Substituicao ,
CAST(Motivo AS STRING)  AS Motivo ,
CAST(Retificacao AS BOOL)  AS Retificacao ,
CAST(RetificacaoTotal AS BOOL)  AS Retificacao_Total ,
CAST(RecalculoDarm_Liberado AS BOOL)  AS Recalculo_DARM_Liberado 
FROM `rj-smdue.adm_licenca_urbanismo_staging.licenca_substituida`