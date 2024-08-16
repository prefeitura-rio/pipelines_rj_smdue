SELECT
num_lic AS Id_Licenciamento,
LotesVinculados  AS Descricao_Lotes_Vinculados ,
CAST(ComprLograProjetados AS FLOAT64) AS Comprimento_Logradouros_Projetados,
CAST(TotalLotesPrimitivosRemembramento AS INT64) AS Total_Lotes_Primitivos_Remembramento,
CAST(TotalLotesRemembrados AS INT64)  AS Total_Lotes_Remembrados ,
CAST(TotalLotesPrimitivosDesmembramento AS INT64)  AS Total_Lotes_Primitivos_Desmembramento ,
CAST(TotalLotesDesmembrados AS INT64) AS Total_Lotes_Desmembrados,
CAST(TotalLotesPrimitivosReDesmembramento AS INT64)  AS Total_Lotes_Primitivos_Remembramento_Desmembramento ,
CAST(TotalLotesReDesmembrados AS INT64)  AS Total_Lotes_Remembramento_Desmembramento ,
CAST(TotalAreasPrivativasPrimitivas AS INT64)  AS Total_Areas_Privativas_Primitivas ,
CAST(TotalAreasPrivativasResultantes AS FLOAT64) AS Total_Areas_Privativas_Resultantes
FROM `rj-smdue.adm_licenca_urbanismo_staging.loteamento_alvara`