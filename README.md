# BrasilAPI Bancos Pipeline

## Objetivo
Pipeline de Engenharia de Dados para extração, armazenamento, transformação, validação e carga de dados de instituições bancárias disponíveis na BrasilAPI

## Arquitetura
![Arquitetura do pipeline](./docs/Arquitetura%20BrasilAPI.png)

O pipeline extrai dados da BrasilAPI, preserva a resposta original em JSON na camada `raw`, transforma e valida os dados, salva a versão tratada em CSV na camada `processed` e, por fim, carrega os registros no PostgreSQL.

## Fluxo do Pipeline
1. Extração dos dados da BrasilAPI
2. Armazenamento do JSON original na camada `raw`
3. Transformação e padronização dos dados com Pandas
4. Validação dos dados tratados
5. Armazenamento do CSV tratado na camada `processed`
6. Carga dos dados no PostgreSQL
7. Inserção e atualização dos registros utilizando `UPSERT` com base no `ispb`

## Decisões Técnicas
- O JSON original é preservado na camada `raw`
- A camada `processed` contém os dados tratados e padronizados
- O campo `ispb` é tratado como texto por representar um identificador
- Valores ausentes em `code` são preservados como `NULL`
- O PostgreSQL utiliza `UPSERT` com `ON CONFLICT` para evitar duplicidade de registros
- Credenciais do banco são armazenadas em variáveis de ambiente

## Estrutura das Pastas
```text
brasilapi-bancos-pipeline/
├── data_lake/
│   ├── raw/
│   └── processed/
├── docs/
│   └── Arquitetura BrasilAPI.png
├── db_connection.py
├── extract.py
├── load.py
├── logging_config.py
├── main.py
├── transform.py
├── validate.py
├── requirements.txt
├── .env.example
└── README.md
```

## Tecnologias
- Python
- Pandas
- PostgreSQL
- Psycopg
- Requests
- python-dotenv

## Como executar
1. Clone o repositório 
```bash
git clone git@github.com:samuellcardoso/brasilapi-bancos-pipeline.git
```
2. Crie e ative o ambiente virtual
```bash
python -m venv .venv
.venv/Scripts/activate
```
3. Instale as dependências
```bash
pip install -r requirements.txt
```
4. Crie um arquivo `.env` com base no `.env.example`

5. Crie o banco de dados no PostgreSQL
```sql
CREATE DATABASE banco;
```
6. Execute o pipeline
```bash
python main.py
```

## Melhorias Futuras
- Automatizar a execução do pipeline
- Adicionar testes automáticos
- Utilizar Docker
- Migrar o armazenamento para AWS
- Adicionar monitoramento das execuções