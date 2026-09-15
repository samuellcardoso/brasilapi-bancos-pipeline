import os
import json
from logging_config import logger
from extract import extract_files
from transform import transform, save_processed
from validate import validate
from load import load

def main(url):
    logger.info('Iniciando Pipeline')

    # Extracao
    dados_extraidos = extract_files(url)
    if not dados_extraidos:
        logger.error('Falha na extracao dos dados.')
        return

    nome_arquivo_json = 'bancos.json'
    diretorio_raw = './data_lake/raw/'
    caminho_raw = os.path.join(diretorio_raw, nome_arquivo_json)

    os.makedirs(diretorio_raw, exist_ok=True)

    with open(caminho_raw, 'w', encoding='utf-8') as arquivo:
        json.dump(dados_extraidos, arquivo, indent=4, ensure_ascii=False)

    logger.info(f'Arquivo raw salvo em {caminho_raw}')
    logger.info('Extracao finalizada')

    # Transformacao
    dados_transformados = transform(caminho_raw)
    if dados_transformados is not None:
        nome_arquivo_csv = 'bancos.csv'
        diretorio_processed = './data_lake/processed/'
        caminho_processed = os.path.join(diretorio_processed, nome_arquivo_csv)

        # Validacao
        dados_validos = validate(dados_transformados)
        if dados_validos:
            logger.info('Dados validos')    
            logger.info('Validacao finalizada')
        else:
            logger.error('Dados invalidos')
            return

        save_processed(dados_transformados, diretorio_processed, caminho_processed)
        
        logger.info('Transformacao finalizada')
    else:
        logger.error('Falha na transformacao dos dados')
        return
        
    # Carregamento
    dados_carregados = load(dados_transformados)
    if dados_carregados:
        logger.info('Carregamento finalizado')
        logger.info('Pipeline finalizado com sucesso')
    else:
        logger.error('Falha no carregamento dos dados')
        return


if __name__ == '__main__':
    url = 'https://brasilapi.com.br/api/banks/v1'
    main(url)