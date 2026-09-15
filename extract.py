import requests
from logging_config import logger

def extract_files(url) -> list:
    logger.info('Iniciando extracao dos dados')

    try:
        response = requests.get(url)
        logger.info('API acessada com sucesso.')
    except Exception as e:
        logger.error(f'Erro ao acessar a API: {e}')
        return None

    if response.status_code == 200:
        try:
            response_json = response.json()
            logger.info('Dados extraidos da API')
            logger.info(f'{len(response_json)} registros encontrados')
            return response_json
        except Exception as e:
            logger.error(f'Erro na extracao dos dados da API: {e}')
            return None
    elif response.status_code == 404:
        logger.error('Dados da API nao encontrados')
        return None
    elif response.status_code == 500:
        logger.error('Erro no servidor interno')
        return None
    else:
        logger.error(f'API retornou status code {response.status_code}')
        return None