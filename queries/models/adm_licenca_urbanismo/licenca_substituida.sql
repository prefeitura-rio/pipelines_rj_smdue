SELECT
num_lic_substituida AS id_licenciamento_substituido,
num_lic_nova AS id_licenciamento_novo,
CAST(dtsubstituicao AS DATETIME) AS data_substituicao,
CAST(motivo AS STRING) AS motivo,
CAST(retificacao AS BOOL) AS retificacao,
CAST(retificacaototal AS BOOL) AS retificacao_total,
CAST(recalculodarm_liberado AS BOOL) AS recalculo_darm_liberado
FROM `rj-smdue.adm_licenca_urbanismo_staging.licenca_substituida`
