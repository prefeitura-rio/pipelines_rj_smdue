SELECT
CAST(id_processo AS STRING) AS id_processo,
CAST(id_processo_sislic AS STRING) AS id_processo_sislic,
CAST(nu_processo AS STRING) AS numero_processo,
CAST(cd_logradouro AS STRING) AS cd_logradouro,
CAST(nu_porta AS STRING) AS numero_porta,
CAST(nu_pal AS STRING) AS numero_pal,
CAST(id_bairro_sislic AS STRING) AS id_bairro_sislic,
CAST(id_ra_sislic AS STRING) AS id_ra_sislic,
CAST(no_bairro AS STRING) AS nome_bairro,
CAST(shape AS GEOGRAPHY) AS coordenadas
FROM `rj-smdue.adm_licenca_urbanismo_staging.georeferencia_endereco_obra_processo`
