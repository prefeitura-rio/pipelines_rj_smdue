SELECT
id_edif AS Id_Edificacao,
Num_Edif  AS Identicacao_Edificacao,
Num_lic AS Id_Licenciamento,
Cod_Tp_edif  AS ID_Tipo_Edificacao ,
cod_Compl_Tp_Edif  AS Id_Complemento_Tipo_Edificacao ,
cod_Compl_Tp_Edif2  AS Id_Complemento_Tipo_Edificacao_2 ,
Compl_Livre AS Complemento,
CAST(area_edif AS FLOAT64)  AS Area_Edificacao ,
CAST(area_acresc AS FLOAT64)  AS Area_Acrescida ,
CAST(area_reduzida AS FLOAT64)  AS Area_Reduzida ,
CAST(area_util AS FLOAT64)  AS Area_Util ,
CAST(embasamento AS BOOL)  AS Embasamento ,
CAST(RecebeNumeracao AS BOOL)  AS Recebe_Numeracao ,
CAST(ContaEdificacao AS BOOL)  AS Conta_Edificacao ,
CAST(Qtd_Edif AS INT64)  AS Total_Edificacoes 
FROM `rj-smdue.adm_licenca_urbanismo_staging.edificacao_obra_licenca`