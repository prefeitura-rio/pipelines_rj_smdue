SELECT
codTramite AS Id_Tramite,
matricCadastrador AS Matricula_Cadastrador,
codDocumento AS Id_Documento,
CAST(dtCadastro AS DATETIME) AS Data_Cadastro,
CAST(dtSaida AS DATETIME) AS Data_Saida,
CAST(vfDestinoOrgao AS BOOL) AS Orgao_Destino,
codDestino AS Id_Orgao_Destino,
matricOrigem AS Matricula_Origem,
matricDestino AS Matricula_Destino,
codOrigem AS Id_Origem,
status AS Status
FROM `rj-smdue.adm_licenca_urbanismo_staging.tramite_processo`