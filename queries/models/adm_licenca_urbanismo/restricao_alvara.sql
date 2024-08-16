SELECT
CAST(CAST(Id_Rest AS FLOAT64) AS int64 ) AS Id_Restricao,
CAST(CAST(num_lic AS FLOAT64) AS INT64) AS Id_Licenciamento,
CAST(CAST(cod_Restricao AS FLOAT64) AS INT64) AS Id_Tipo_Restricao,
CAST(Compl_Restricao  AS string) AS Compl_Tipo_Restricao ,
CAST(Outra_restricao  AS string) AS Outra_restricao ,
CAST(Data_Baixa  AS datetime) AS Data_Baixa ,
CAST(BAIXA_EXOFFICIO  AS string) AS Baixa_EXOFFICIO 
FROM `rj-smdue.adm_licenca_urbanismo_staging.restricao_alvara`