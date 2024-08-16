SELECT
Id_Lic  AS Id_Licenca,
num_lic  AS Id_Licenciamento,
id_edif  AS Id_Edificacao ,
cod_classe  AS Id_Classe_Licenca ,
cod_tipo_lic  AS Id_Tipo_Licenca ,
cod_lic  AS cod_lic ,
cod_compl_lic  AS Id_Complemento_Tipo_Licenca ,
Compl_Livre  AS Comentario_Licenca,
CAST(Dec9218 AS BOOL) AS Decreto_9218,
OutroDec  AS Outro_Decreto ,
CAST(ObrasConcluidas AS BOOL)  AS Obras_Concluidas 
FROM `rj-smdue.adm_licenca_urbanismo_staging.licenca_alvara`