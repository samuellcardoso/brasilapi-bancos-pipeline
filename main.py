import os
import json

from logging_config import logger
from extract import extract_files
from transform import transform, save_processed
from validate import validate
from load import load


def main(url):
    logger.info('Iniciando pipeline BrasilAPI Bancos')

    # Extract: captura a resposta da API e preserva o JSON na camada raw.
    dados_extraidos = extract_files(url)
    if not dados_extraidos:
        logger.error('Extracao sem dados: pipeline interrompido')
        return

    diretorio_raw = './data_lake/raw/'
    caminho_raw = os.path.join(diretorio_raw, 'bancos.json')
    os.makedirs(diretorio_raw, exist_ok=True)

    with open(caminho_raw, 'w', encoding='utf-8') as arquivo:
        json.dump(dados_extraidos, arquivo, indent=4, ensure_ascii=False)
    logger.info('Arquivo raw salvo em %s', caminho_raw)

    # Transform + Validate: impede que dados invalidos sejam carregados.
    dados_transformados = transform(caminho_raw)
    if dados_transformados is None:
        logger.error('Falha na transformacao: pipeline interrompido')
        return

    if not validate(dados_transformados):
        logger.error('Dados invalidos: pipeline interrompido')
        return

    diretorio_processed = './data_lake/processed/'
    caminho_processed = os.path.join(diretorio_processed, 'bancos.csv')
    if not save_processed(dados_transformados, diretorio_processed, caminho_processed):
        logger.error('Falha ao salvar camada processed: pipeline interrompido')
        return

    # Load: tabela dim_bancos no PostgreSQL.
    if load(dados_transformados):
        logger.info('Pipeline concluido com sucesso')
    else:
        logger.error('Falha no carregamento dos dados')


if __name__ == '__main__':
    main('https://brasilapi.com.br/api/banks/v1')
