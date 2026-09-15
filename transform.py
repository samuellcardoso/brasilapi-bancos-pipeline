import pandas as pd
import os 
from logging_config import logger

def transform(json_path) -> pd.DataFrame:
    logger.info('Iniciando Transformacao dos dados')
    
    try:
        df = pd.read_json(json_path)
    except Exception as e:
        logger.error(f'Erro ao ler arquivo JSON: {e}')
        return None
    else:
        novo_df = df[['ispb', 'name', 'code', 'fullName']].rename(
            columns={'fullName':'full_name'}
        )
        logger.info('Dataframe criado com colunas selecionadas')
        
        novo_df = novo_df.drop_duplicates()
        logger.info('Dados duplicados excluidos')
        
        novo_df['name'] = novo_df['name'].str.upper()
        novo_df['full_name'] = novo_df['full_name'].str.upper()
        logger.info('Coluna "name e full_name" renomeada para UPPER')
        
        novo_df['ispb'] = novo_df['ispb'].astype(str)
        novo_df['code'] = novo_df['code'].astype('Int64') 
        logger.info('Tipos atribuidos as colunas "ispb e code"')     
        
        novo_df['name'] = novo_df['name'].str.strip()
        novo_df['full_name'] = novo_df['full_name'].str.strip()
        logger.info('Espacos removidos')

        return novo_df


def save_processed(df, diretorio ,arquivo):
    try:
        if df is None:
            logger.error('Arquivo nao existe')
            return None
        
        if df.empty:
            logger.error('Arquivo esta vazio')
            return None
    except Exception as e:
        logger.error(f'Erro ao validar DataFrame: {e}')
    else:
        os.makedirs(diretorio, exist_ok=True)
        df.to_csv(arquivo, index=False, encoding='utf-8')
        logger.info('Dados transformados com sucesso')
        logger.info(f'Arquivo salvo em {arquivo}')
        
        return arquivo