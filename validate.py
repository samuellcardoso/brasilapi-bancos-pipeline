import pandas as pd
from logging_config import logger


def validate(df: pd.DataFrame) -> bool:
    logger.info('Iniciando validacao dos dados')

    if df is None or df.empty:
        logger.error('DataFrame ausente ou vazio')
        return False

    colunas_obrigatorias = ['ispb', 'name', 'code', 'full_name']
    colunas_ausentes = [coluna for coluna in colunas_obrigatorias if coluna not in df.columns]
    if colunas_ausentes:
        logger.error('Colunas ausentes: %s', colunas_ausentes)
        return False

    campos_nao_nulos = ['ispb', 'name', 'full_name']
    if df[campos_nao_nulos].isna().any().any():
        logger.error('Campos obrigatorios contem valores nulos')
        return False

    for coluna in campos_nao_nulos:
        if df[coluna].astype('string').str.strip().eq('').any():
            logger.error('Coluna %s contem valores vazios', coluna)
            return False

    if df['ispb'].duplicated().any():
        logger.error('A coluna ispb contem valores duplicados')
        return False

    for coluna in ['ispb', 'name', 'full_name']:
        if not pd.api.types.is_string_dtype(df[coluna]):
            logger.error('A coluna %s deve ter tipo texto', coluna)
            return False

    if not pd.api.types.is_integer_dtype(df['code']):
        logger.error('A coluna code deve ter tipo inteiro (aceitando nulos)')
        return False

    logger.info('Validacao concluida com sucesso | registros=%s', len(df))
    return True
