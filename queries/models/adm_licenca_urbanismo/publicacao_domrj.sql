SELECT
codpublicacao AS id_publicacao,
CAST(dtenvio AS DATETIME) AS data_envio,
CAST(dtpublicacao AS DATETIME) AS data_publicacao,
CAST(dtprevista AS DATETIME) AS data_prevista
FROM `rj-smdue.adm_licenca_urbanismo_staging.publicacao_domrj`
