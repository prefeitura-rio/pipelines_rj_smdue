SELECT
    Num_Aceitacao AS id_aceitacao,
    Num_Proc AS numero_processo,
    Num_Lic AS id_licenciamento,
    Cod_DLF AS id_orgao_SISLIC,
    CAST(Dt_Emissao AS DATETIME) AS data_emissao,
    CAST(Dt_Certidao AS DATETIME)  AS data_certidao,
    Matricula_RGI AS matricula_rgi,
    Nr_Oficio_RGI AS numero_oficio_rgi,
    PAL AS numero_PAL,
    Mat_Tec_Resp AS matricula_tecnico_responsavel,
    CAST(Cancelado AS BOOL) AS cancelado,
    Obs AS observacao
FROM `rj-smdue.adm_licenca_urbanismo_staging.certidao_aceitacao`