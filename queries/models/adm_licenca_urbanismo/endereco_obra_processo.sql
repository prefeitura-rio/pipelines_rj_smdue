SELECT
codDocumento AS id_documento,
codEndereco AS id_endereco,
CAST(vfPrincipal AS BOOL) AS endereco_principal,
matricCadastrador AS matricula_cadastrador,
CAST(dtCadastro AS datetime) AS data_cadastro
FROM `rj-smdue.adm_licenca_urbanismo_staging.endereco_obra_processo`