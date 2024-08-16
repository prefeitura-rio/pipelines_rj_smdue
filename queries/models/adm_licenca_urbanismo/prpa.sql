SELECT
    ID_PRPA AS id_PRPA,
    CODDOCUMENTO AS id_Processo,
    NOME_PRPA AS nome_PRPA,
    CPF_PRPA AS CPF_PRPA,
    EMAIL_PRPA AS email_PRPA,
    TELEFONE_PRPA AS telefone_PRPA,
    TIPO_REGISTRO_PRPA AS Tipo_Registro_PRPA,
    NUMERO_REGISTRO_PRPA AS Numero_Registro_PRPA,
    TIPO_CONSELHO_PRPA AS Tipo_Conselho_PRPA,
    NUMERO_CONSELHO_PRPA AS Numero_Conselho_PRPA,
    CAST(ID_PROFISSAO AS INT64) AS Id_Profissao
FROM `rj-smdue.adm_licenca_urbanismo_staging.prpa`