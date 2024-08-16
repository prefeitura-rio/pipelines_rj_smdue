SELECT
    Cod_Fase AS id_fase,
    Abrev_Fase AS nome_fase,
    CAST(OrdemImp AS INT64) AS ordem_importancia
FROM `rj-smdue.adm_licenca_urbanismo_staging.fase_obra`