SELECT
codLinha AS Id_Linha,
codTramite AS Id_Tramite,
codPublicacao AS Id_Publicacao,
codOrgao AS Id_Orgao,
descTipoDespacho AS Descricao_Tipo_Despacho,
numero AS Numero_Documento,
texto AS Texto,
texto_final AS Texto_Final,
requerente AS Nome_Requerente,
matricLiberador AS Matricula_Liberador,
CAST(dtCadastro AS DATETIME) AS Data_Cadastro,
CAST(dtExpediente AS DATETIME) AS Data_Expediente,
CAST(dtliberacao AS DATETIME) AS Data_Liberacao
FROM `rj-smdue.adm_licenca_urbanismo_staging.linha_publicacao_tramite`