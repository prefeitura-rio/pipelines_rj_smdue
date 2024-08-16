SELECT
num_Darm AS Id_Darm,
DARM  AS Numero_DARM ,
Num_Lic  AS Id_Licenciamento,
CNPJ_CPF  AS CNPJ_CPF ,
Cod_Receita  AS Codigo_Receita ,
CAST(Dt_Emissao AS DATETIME)  AS Data_Emissao ,
CAST(Dt_Venc AS DATETIME)  AS Data_Vencimento ,
CAST(Dt_Pagamento AS DATETIME)  AS Data_Pagamento ,
CAST(Competencia AS INT64)  AS Competencia ,
CAST(Mora AS FLOAT64)  AS Mora ,
CAST(Multa AS FLOAT64) AS Multa,
CAST(Valor_Darm_Inicial AS FLOAT64)  AS Valor_Darm_Inicial ,
CAST(ValorDarm AS FLOAT64)  AS Valor_Darm ,
CAST(Cancelado AS BOOl)  AS Cancelado ,
CAST(Dt_Calculo AS DATETIME)  AS Data_Calculo ,
CAST(InscIPTU AS STRING)  AS Numero_Inscricao_Imovel_IPTU ,
CAST(Avulso AS BOOL)  AS DARM_Avulso 
FROM `rj-smdue.adm_licenca_urbanismo_staging.darm_alvara`