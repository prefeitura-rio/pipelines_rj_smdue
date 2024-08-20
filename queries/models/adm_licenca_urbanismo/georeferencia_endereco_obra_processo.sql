SELECT
CAST(id_processo AS STRING) AS Id_Processo,
CAST(id_processo_sislic AS STRING) AS Id_Processo_Sislic,
CAST(nu_processo AS STRING) AS Numero_Processo,
CAST(cd_logradouro AS STRING) AS Cd_Logradouro,
CAST(nu_porta AS STRING) AS numero_porta,
CAST(nu_pal AS STRING) AS Numero_PAL,
CAST(id_bairro_sislic AS STRING) AS Id_Bairro_SISLIC,
CAST(id_ra_sislic AS STRING) AS Id_RA_SISLIC,
CAST(no_bairro AS STRING) AS Nome_Bairro,
CAST(shape AS GEOGRAPHY) AS Coordenadas
FROM `rj-smdue.adm_licenca_urbanismo_staging.georeferencia_endereco_obra_processo`