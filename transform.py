import os
import pandas as pd
from logging_config import logger


def transform(json_path) -> pd.DataFrame | None:
    logger.info('Iniciando transformacao dos dados')

    try:
        df = pd.read_json(json_path, dtype={'ispb': 'string'})
        novo_df = df[['ispb', 'name', 'code', 'fullName']].copy()
        novo_df = novo_df.rename(columns={'fullName': 'full_name'})
        novo_df = novo_df.drop_duplicates()

        # Preserva identificadores como texto (inclusive zeros a esquerda).
        novo_df['ispb'] = novo_df['ispb'].astype('string')
        novo_df['name'] = novo_df['name'].astype('string').str.upper().str.strip()
        novo_df['full_name'] = novo_df['full_name'].astype('string').str.upper().str.strip()
        novo_df['code'] = pd.to_numeric(novo_df['code'], errors='raise').astype('Int64')

        logger.info('Transformacao concluida | registros=%s', len(novo_df))
        return novo_df

    except Exception:
        logger.exception('Falha na transformacao dos dados')
        return None


def save_processed(df: pd.DataFrame, diretorio: str, arquivo: str) -> str | None:
    if df is None or df.empty:
        logger.error('Nao ha dados validos para salvar na camada processed')
        return None

    try:
        os.makedirs(diretorio, exist_ok=True)
        df.to_csv(arquivo, index=False, encoding='utf-8')
        logger.info('Arquivo processed salvo em %s', arquivo)
        return arquivo

    except Exception:
        logger.exception('Erro ao salvar arquivo processed')
        return None
