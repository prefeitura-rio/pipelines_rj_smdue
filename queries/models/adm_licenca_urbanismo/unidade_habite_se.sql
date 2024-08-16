SELECT
    ID AS id_unidades_habite_se,
    Num_Hab AS id_habite_se,
    Id_edif AS id_edificacao,
    CAST(Quant_Edif AS INT64) AS quantidade_edificacoes,
    Cod_Unidade AS id_unidade,
    CAST(Quant_Unidade AS INT64) AS quantidade_unidades,
    CAST(Area AS FLOAT64) AS area
FROM `rj-smdue.adm_licenca_urbanismo_staging.unidade_habite_se`