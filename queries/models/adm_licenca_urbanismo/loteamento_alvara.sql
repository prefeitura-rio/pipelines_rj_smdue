SELECT
num_lic AS Id_Licenciamento,
LotesVinculados  AS Descricao_Lotes_Vinculados ,
CAST(ComprLograProjetados AS FLOAT64) AS Comprimento_Logradouros_Projetados,
CAST(CAST(TotalLotesPrimitivosRemembramento AS FLOAT64) AS INT64) AS Total_Lotes_Primitivos_Remembramento,
CAST(CAST(TotalLotesRemembrados AS FLOAT64) AS INT64)  AS Total_Lotes_Remembrados ,
CAST(CAST(TotalLotesPrimitivosDesmembramento AS FLOAT64) AS INT64)  AS Total_Lotes_Primitivos_Desmembramento ,
CAST(CAST(TotalLotesDesmembrados AS FLOAT64) AS INT64) AS Total_Lotes_Desmembrados,
CAST(CAST(TotalLotesPrimitivosReDesmembramento AS FLOAT64) AS INT64)  AS Total_Lotes_Primitivos_Remembramento_Desmembramento ,
CAST(CAST(TotalLotesReDesmembrados AS FLOAT64) AS INT64)  AS Total_Lotes_Remembramento_Desmembramento ,
CAST(CAST(TotalAreasPrivativasPrimitivas AS FLOAT64) AS INT64)  AS Total_Areas_Privativas_Primitivas ,
CAST(TotalAreasPrivativasResultantes AS FLOAT64) AS Total_Areas_Privativas_Resultantes
FROM `rj-smdue.adm_licenca_urbanismo_staging.loteamento_alvara`