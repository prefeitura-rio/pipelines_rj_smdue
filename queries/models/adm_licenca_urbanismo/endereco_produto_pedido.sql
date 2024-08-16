SELECT
codEndereco AS Id_Endereco,
codLogra AS Id_Logradouro,
numPorta AS Numero_Porta,
complPorta AS Complemento_Porta,
codBairro AS Id_Bairro,
numPAL AS Numero_PAL,
numQuadra AS Numero_Quadra,
numLote AS Numero_Lote,
CAST(vfMunicipal AS BOOL) AS Endereco_Dentro_Municipio,
UF AS UF,
numPAA AS Numero_PAA,
CAST(dtCadastro AS DATETIME) AS Data_Cadastro,
CAST(CAST(matricCadastrador AS FLOAT64) AS INT64) AS Matricula_Cadastrador,
CEP AS CEP,
InscricaoIMOVEL AS Inscricao_Imovel,
CAST(CAST(ID_TpInscricaoIMOVEL AS FLOAT64) AS INT64) AS ID_Tipo_Inscricao_Imovel
FROM `rj-smdue.adm_licenca_urbanismo_staging.endereco_produto_pedido`