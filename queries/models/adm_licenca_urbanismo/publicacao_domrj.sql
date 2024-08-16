SELECT
codPublicacao AS Id_Publicacao,
CAST(dtEnvio AS DATETIME) AS Data_Envio,
CAST(dtPublicacao AS DATETIME) AS Data_Publicacao,
CAST(dtPrevista AS DATETIME) AS Data_Prevista
FROM `rj-smdue.adm_licenca_urbanismo_staging.publicacao_domrj`