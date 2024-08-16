SELECT
    CodOrgao AS id_orgao_SMU,
    CodOrgaoSigma AS id_orgao_SISLIC,
    CAST(Ativo AS BOOL) AS ativo
FROM `rj-smdue.adm_licenca_urbanismo_staging.orgao_licenciamento`