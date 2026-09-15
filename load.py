from logging_config import logger
import pandas as pd
from db_connection import conn

def load(df):
    logger.info('Iniciando carregamento dos dados')
        
    with conn.cursor() as cursor:
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dim_bancos (
                    id SERIAL PRIMARY KEY,
                    ispb VARCHAR(30) UNIQUE NOT NULL,
                    name VARCHAR(150) NOT NULL,
                    code INT,
                    full_name VARCHAR(255) NOT NULL
                )
                        ''')
        except Exception as e:
            logger.error(f'Erro ao criar a tabela: {e}')
            conn.rollback()
            return False
        else:
            logger.info('Tabela criada com sucesso')
            
        try:
            for _, dado in df.iterrows():
                code = None if pd.isna(dado['code']) else int(dado['code'])
                
                cursor.execute('''
                    INSERT INTO dim_bancos (
                        ispb,
                        name,
                        code,
                        full_name
                    ) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT(ispb)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        code = EXCLUDED.code,
                        full_name = EXCLUDED.full_name
            ''',(dado['ispb'],
                    dado['name'],
                    code,
                    dado['full_name'])
            )
        except Exception as e:
            logger.error(f'Erro ao inserir os dados: {e}')
            conn.rollback()
            return False
        else:
            conn.commit()
            logger.info(f'{len(df)} dados carregados no PostgreSQL')
            return True
            
    conn.close()