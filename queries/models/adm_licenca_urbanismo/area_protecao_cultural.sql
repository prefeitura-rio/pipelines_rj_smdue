SELECT
ID_AREA_PROTECAO_CULTURAL AS id_area_protecao_cultural,
REGEXP_REPLACE(
    NORMALIZE(UPPER(DS_AREA_PROTECAO_CULTURAL), NFD),
    r'\p{M}',
    ''
  ) AS nome_area_protecao_ambiental
FROM `rj-smdue.adm_licenca_urbanismo_staging.area_protecao_cultural`