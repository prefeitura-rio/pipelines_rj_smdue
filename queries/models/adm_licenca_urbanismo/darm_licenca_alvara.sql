SELECT
Num_Darm  AS Id_Darm ,
cod_Classe  AS Id_Classe_Licenca ,
cod_Tipo_Lic  AS Id_Tipo_Licenca ,
cod_Lic  AS cod_Lic,
cod_Compl_Lic  AS Id_Complemento_Tipo_Licenca ,
compl_Livre  AS Comentario_Licenca,
CAST(Valor AS FLOAT64)  AS Valor ,
Formula  AS Formula 
FROM `rj-smdue.adm_licenca_urbanismo_staging.darm_licenca_alvara`