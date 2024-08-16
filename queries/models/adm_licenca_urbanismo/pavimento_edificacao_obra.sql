SELECT
Id_Pav AS Id_Pavimento,
Num_lic AS Id_Licenciamento,
Id_Edif AS Id_Edificacao,
Pavimento  AS Pavimento ,
CAST(Tot_pav AS INT64)  AS Total_Pavimentos,
CAST(tot_vagasCobertas AS INT64) AS Total_Vagas_Cobertas,
CAST(Tot_VagasDescobertas AS INT64)  AS Total_Vagas_Descobertas 
FROM `rj-smdue.adm_licenca_urbanismo_staging.pavimento_edificacao_obra`