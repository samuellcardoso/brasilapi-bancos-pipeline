# BrasilAPI Bancos | Pipeline de Engenharia de Dados

Pipeline **ETL em Python** que consulta a [BrasilAPI](https://brasilapi.com.br/), preserva os dados originais, realiza transformações e validações com Pandas e atualiza uma tabela no PostgreSQL.

Este projeto demonstra um fluxo de ponta a ponta, com separação de responsabilidades, rastreabilidade por logs e carga repetível com `UPSERT`.

## Arquitetura

![Arquitetura do pipeline](./docs/Arquitetura%20BrasilAPI.png)

```text
BrasilAPI (GET /api/banks/v1)
          |
          v
   Extracao com Requests
          |
          v
 data_lake/raw/bancos.json
          |
          v
 Transformacao com Pandas
          |
          v
   Validacao dos dados
          |
          v
data_lake/processed/bancos.csv
          |
          v
     Carga com Psycopg
          |
          v
 PostgreSQL (dim_bancos)
```

O `main.py` coordena todas as etapas. O armazenamento em `raw` e `processed` é **local**; o projeto não utiliza serviços AWS nesta versão.

## Fonte de dados

- **Origem:** [BrasilAPI — Bancos](https://brasilapi.com.br/docs#tag/BANKS)
- **Endpoint:** `https://brasilapi.com.br/api/banks/v1`
- **Formato de origem:** JSON
- **Destino:** tabela `dim_bancos` no PostgreSQL

A extração é automática durante a execução do pipeline, portanto não é necessário baixar o JSON manualmente.

## Fluxo do pipeline

1. **Extract:** requisita os bancos à API e salva a resposta em `data_lake/raw/bancos.json`.
2. **Transform:** seleciona as colunas relevantes, remove linhas inteiramente duplicadas, padroniza textos e ajusta os tipos.
3. **Validate:** verifica estrutura, campos obrigatórios, unicidade de `ispb` e tipos esperados.
4. **Processed:** salva os dados validados em `data_lake/processed/bancos.csv`.
5. **Load:** cria a tabela `dim_bancos` caso ela não exista e insere/atualiza os registros no PostgreSQL.

Os módulos registram informações de execução e erros por meio de `logging`.

## Modelo de dados

| Coluna | Tipo no PostgreSQL | Descrição |
| --- | --- | --- |
| `id` | `SERIAL PRIMARY KEY` | Chave interna da tabela |
| `ispb` | `VARCHAR(30) UNIQUE NOT NULL` | Identificador do banco e chave de conflito |
| `name` | `VARCHAR(150) NOT NULL` | Nome abreviado, padronizado |
| `code` | `INT NULL` | Código bancário, quando informado pela API |
| `full_name` | `VARCHAR(255) NOT NULL` | Nome completo, padronizado |

**Granularidade:** cada linha representa uma instituição bancária identificada pelo `ispb`.

### Decisões técnicas

- O JSON original é preservado na camada `raw`; o CSV padronizado é salvo na `processed`.
- O `ispb` é tratado como **texto**, pois é um identificador, não uma medida numérica.
- O campo `code` admite valores nulos.
- A validação impede a carga de dados incompletos, duplicados ou com tipos incompatíveis.
- O `UPSERT` com `ON CONFLICT (ispb)` atualiza registros existentes, sem inserir outra linha com o mesmo identificador.
- As credenciais são lidas de variáveis de ambiente, sem senhas no código.
- As etapas estão separadas em módulos e são orquestradas pelo `main.py`.

## Estrutura do projeto

```text
brasilapi-bancos-pipeline/
├── data_lake/
│   ├── raw/
│   │   └── bancos.json
│   └── processed/
│       └── bancos.csv
├── docs/
│   └── Arquitetura BrasilAPI.png
├── tests/
│   └── test_validate.py
├── db_connection.py
├── extract.py
├── load.py
├── logging_config.py
├── main.py
├── transform.py
├── validate.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Tecnologias

**Python · Pandas · Requests · Psycopg 3 · PostgreSQL · python-dotenv · Git/GitHub**

Também são utilizados módulos da biblioteca padrão do Python, como `logging`, `json` e `os`.

## Como executar

**Pré-requisitos:** Python, PostgreSQL instalado e acesso à internet para consultar a BrasilAPI.

**1. Clonar o projeto**

```bash
git clone https://github.com/samuellcardoso/brasilapi-bancos-pipeline.git
cd brasilapi-bancos-pipeline
```

**2. Preparar o ambiente Python**

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Depois, instalar as dependências:

```bash
pip install -r requirements.txt
```

**3. Configurar o PostgreSQL**

Crie o banco de dados (por exemplo, no pgAdmin ou no `psql`):

```sql
CREATE DATABASE banco;
```

Copie `.env.example` para um novo arquivo `.env` e preencha com seus dados locais:

```dotenv
DB_NAME=banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

**Não envie o `.env` com credenciais reais para o GitHub.** A tabela `dim_bancos` é criada automaticamente na primeira execução.

**4. Executar o pipeline**

```bash
python main.py
```

Ao concluir, confira os arquivos das camadas `raw` e `processed`. Para verificar a carga no banco:

```sql
SELECT COUNT(*) FROM dim_bancos;

SELECT ispb, name, code, full_name
FROM dim_bancos
ORDER BY name
LIMIT 10;
```

Reexecutar o pipeline deve atualizar os bancos já cadastrados com base em `ispb`, sem duplicá-los.

**5. Executar os testes unitários de validação**

```bash
python -m unittest discover -s tests -v
```

Esses testes não exigem conexão com a API nem com PostgreSQL.

## Limites e próximos passos

Este é um projeto introdutório de ETL, com execução manual e persistência em PostgreSQL local. Possíveis evoluções:

- Agendar a execução do pipeline.
- Aumentar a cobertura de testes, incluindo integração com banco e API.
- Adicionar métricas de execução e monitoramento.
- Utilizar Docker para facilitar a instalação.
- Experimentar armazenamento e processamento em nuvem (AWS).

---

**Propósito no portfólio:** demonstrar fundamentos de integração com APIs, Data Lake local, qualidade dos dados e carga idempotente em banco relacional.
