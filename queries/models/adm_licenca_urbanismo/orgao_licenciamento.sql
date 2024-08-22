SELECT
    codorgao AS id_orgao_smu,
    codorgaosigma AS id_orgao_sislic,
    CAST(ativo AS BOOL) AS ativo
FROM `rj-smdue.adm_licenca_urbanismo_staging.orgao_licenciamento`
