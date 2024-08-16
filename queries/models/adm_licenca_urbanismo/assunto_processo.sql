SELECT
    codAssuntoN1 AS id_assunto_nivel_1,
    codAssuntoN2 AS id_assunto_nivel_2,
    codAssuntoN3 AS id_assunto_nivel_3,
    codAssunto AS id_assunto,
    Status AS status,
    codAssunto_ReqOnLine AS id_assunto_requerimento_online,
    CAST(Exige_Endereco AS INT64) AS exige_endereco,
    CAST(Exige_ProcessoConstrucao AS INT64) AS exige_processo_construcao,
    CAST(Exige_CPF_CNPJ_Requerente AS INT64) AS exige_CPF_CNPJ_requerente,
    AssuntoProcessoRio AS assunto_processo_rio
FROM `rj-smdue.adm_licenca_urbanismo_staging.assunto_processo`