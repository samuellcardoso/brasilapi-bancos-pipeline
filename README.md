# BrasilAPI Bancos Pipeline

## Objetivo
Pipeline de dados de extracao, transformacao, validacao e carga de dados bancarios da BrasilAPI.

## Arquitetura
BrasilAPI
-> Raw JSON
-> Transformacao
-> Validacao
-> Processed CSV
-> PostgreSQL

## Tecnologias
- Python
- Pandas
- PostgreSQL
- Psycopg
- Requests
- python-dotenv

## Como executar
1. Criar ambiente virtual
2. Instalar requirements
3. Configurar .env
4. Criar o banco PostgreSQL
5. Executar main.py
