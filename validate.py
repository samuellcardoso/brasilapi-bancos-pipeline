from logging_config import logger
import pandas as pd

def validate(df: pd.DataFrame) -> bool:
    logger.info('Iniciando validacao dos dados')
    
    if df.empty:
        logger.error('Arquivo esta vazio')
        return False
    
    colunas_obrigatorias = ['ispb', 'name', 'code', 'full_name']
    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            logger.error(f'Coluna {coluna} nao esta no arquivo')
            return False
        
    if df['ispb'].isna().any():
        logger.error('A coluna "ispb" contem valores nulos')
        return False

    if df['ispb'].duplicated().any():
        logger.error('A coluna "ispb" contem valores duplicados')
        return False

    if (df['name'].str.strip() == '').any():
        logger.error('A coluna "name" contem valores vazios')
        return False

    colunas_str = ['ispb', 'name', 'full_name']
    for coluna in colunas_str:
        if not pd.api.types.is_string_dtype(df[coluna]):
            logger.error(f'Coluna {coluna} nao estao no tipo "str"')
            return False
    if not pd.api.types.is_integer_dtype(df['code']):
        logger.error('Coluna nao esta no tipo "int"')
        return False
        
    return True