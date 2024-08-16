SELECT
CAST(Id_Lote  AS string) AS id_lote ,
CAST(num_lic AS string) AS id_licenciamento,
CAST(Quantidade  AS int) AS quantidade_lotes,
CAST(Categoria  AS int) AS categoria_lote,
CAST(TpLote  AS int) AS lote_aprovado 
FROM `rj-smdue.adm_licenca_urbanismo_staging.licenca_loteamento`