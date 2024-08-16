SELECT
Id_Unid  AS Id_Unidade,
num_lic AS Id_Licenciamento,
id_edif AS Id_Edificacao,
id_SubDivisao AS id_SubDivisao,
cod_unidade  AS Id_Tipo_Unidade,
ComplTipo_Unid  AS Descricao_Tipo_Unidade ,
CAST(CAST(quant_unid AS FLOAT64) AS INT64)  AS Quantidade_Unidades ,
Num_recebida  AS Identificacao_Unidade ,
CAST(area_unid AS FLOAT64)  AS Area_Unidades 
FROM `rj-smdue.adm_licenca_urbanismo_staging.unidade_edificacao_obra`