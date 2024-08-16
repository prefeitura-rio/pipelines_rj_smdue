SELECT
codParecer AS Id_Parecer,
descParecer AS Descricao_Parecer,
CAST(vfGeraPublicacao as int64) AS Gera_Publicacao,
descClassificacao AS Classificacao,
cast(PUBLICACAO_FRENTE_DO as bool) AS Publicacao_Frente_DO
FROM `rj-smdue.adm_licenca_urbanismo_staging.tipo_parecer_tramite`