import pandas as pd
from logging_config import logger
from db_connection import get_connection


def load(df: pd.DataFrame) -> bool:
    logger.info('Iniciando carregamento dos dados')

    try:
        # A transacao e confirmada ao sair sem erros; em caso de erro ocorre rollback.
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS dim_bancos (
                        id SERIAL PRIMARY KEY,
                        ispb VARCHAR(30) UNIQUE NOT NULL,
                        name VARCHAR(150) NOT NULL,
                        code INT,
                        full_name VARCHAR(255) NOT NULL
                    )
                """)
                logger.info('Tabela dim_bancos criada ou verificada')

                for _, dado in df.iterrows():
                    code = None if pd.isna(dado['code']) else int(dado['code'])
                    cursor.execute("""
                        INSERT INTO dim_bancos (ispb, name, code, full_name)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (ispb)
                        DO UPDATE SET
                            name = EXCLUDED.name,
                            code = EXCLUDED.code,
                            full_name = EXCLUDED.full_name
                    """, (dado['ispb'], dado['name'], code, dado['full_name']))

        logger.info('Carga concluida no PostgreSQL | registros processados=%s', len(df))
        return True

    except Exception:
        logger.exception('Falha ao carregar dados no PostgreSQL')
        return False
