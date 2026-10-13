import requests
from logging_config import logger


def extract_files(url) -> list | None:
    logger.info('Iniciando extracao dos dados')

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        dados = response.json()

        if not isinstance(dados, list):
            logger.error('Resposta da API nao possui o formato esperado (lista)')
            return None

        logger.info('Dados extraidos da API | registros=%s', len(dados))
        return dados

    except requests.RequestException:
        logger.exception('Erro ao acessar a API')
    except ValueError:
        logger.exception('Resposta da API nao contem JSON valido')

    return None
