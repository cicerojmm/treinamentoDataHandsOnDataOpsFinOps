# Treinamento Engenharia de Dados

Projeto completo de engenharia de dados com pipeline de ingestão, processamento e análise usando tecnologias AWS e ferramentas open source.

## 📝 Pré-requisitos

- **AWS CLI** configurado com credenciais
- **Terraform** >= 1.0
- **Docker** e **Docker Compose**
- **Git** para versionamento
- **Python** 3.8+ (para scripts utilitários)

### Configuração Inicial
```bash
# Clone do repositório
git clone <repository-url>
cd treinamentoDataHandsOnDataOpsFinOpsAWS

# Configurar AWS CLI
aws configure

# Verificar credenciais
aws sts get-caller-identity
```

## 🏗️ Arquitetura

### Componentes Principais:
- **PostgreSQL RDS** - Banco de dados transacional
- **DMS Serverless** - Replicação CDC para S3
- **Debezium + Kafka** - Streaming de mudanças em tempo real
- **AWS Glue** - ETL e processamento de dados
- **S3 Tables (Iceberg)** - Data Lake com formato Iceberg
- **Step Functions** - Orquestração de workflows
- **OpenSearch** - Busca e analytics em tempo real
- **EventBridge** - Event-driven architecture
- **Metabase** - Business Intelligence e dashboards

## 📁 Estrutura do Projeto

```
treinamentoDataHandsOnDataOpsFinOpsAWS/
├── terraform/infra/          # Infraestrutura como código
│   ├── modules/             # Módulos Terraform reutilizáveis
│   │   ├── vpc/            # VPC e networking
│   │   ├── rds/            # PostgreSQL RDS
│   │   ├── dms-serverless/ # DMS para CDC
│   │   ├── glue-job/       # Jobs Glue ETL
│   │   ├── glue-crawler/   # Crawlers Glue
│   │   ├── step-functions/ # Orquestração workflows
│   │   ├── lambda_ecr/     # Lambda com Docker
│   │   ├── ec2/            # Instâncias EC2
│   │   └── eventbridge/    # Event-driven architecture
│   ├── scripts/            # Scripts Glue, Lambda e Step Functions
│   │   ├── glue_etl/      # Scripts ETL
│   │   ├── lambda_code_ecr/ # Código Lambda
│   │   └── bootstrap/      # Scripts inicialização
│   ├── envs/              # Configurações por ambiente
│   └── backends/          # Configurações backend Terraform
├── debezium/              # Configuração Debezium + Kafka
│   ├── connect-configs/   # Configurações conectores
│   └── docker-compose.yml # Stack Kafka/Debezium
├── opensearch/            # Stack OpenSearch
├── metabase/              # Business Intelligence
├── jars/                  # JARs para Spark e Debezium
│   ├── debezium/         # JARs Debezium
│   └── spark-streaming/  # JARs Spark Streaming
├── github-actions/        # CI/CD pipelines
└── scripts/              # Scripts utilitários
```

## 🚀 Módulos Terraform

### VPC (`modules/vpc`)
- VPC com subnets públicas e privadas
- Internet Gateway e Route Tables
- VPC Endpoints para S3
- DMS Replication Subnet Group

### RDS PostgreSQL (`modules/rds`)
- Instância PostgreSQL 17.5
- Security Groups configurados
- Parameter Groups customizados
- Configurado para CDC

### DMS Serverless (`modules/dms-serverless`)
- Source Endpoint (PostgreSQL)
- Target Endpoint (S3)
- Replication Task para CDC
- IAM Roles necessárias

### Glue Jobs (`modules/glue-job`)
- Jobs ETL para S3 Tables (Iceberg)
- Processamento de dimensões e fatos
- Data Quality com Great Expectations
- Suporte a JARs customizados

### Step Functions (`modules/step-functions`)
- Orquestração de workflows ETL
- Integração com Glue Jobs
- Logging e monitoramento

### Lambda ECR (`modules/lambda_ecr`)
- Funções Lambda com Docker
- Integração com DuckDB
- Function URLs configuradas

### EC2 (`modules/ec2`)
- Instâncias para processamento
- Security Groups configurados
- Bootstrap scripts

### EventBridge (`modules/eventbridge`)
- Rules para eventos
- Integração com Lambda
- Event-driven architecture

### Glue Crawler (`modules/glue-crawler`)
- Descoberta automática de schemas
- Catalogação de dados S3
- Integração com Glue Data Catalog

## 🔧 Deploy da Infraestrutura

### 1. Configurar Backend
```bash
cd terraform/infra
terraform init -backend-config="backends/develop.hcl"
```

### 2. Aplicar Terraform
```bash
terraform apply -var-file=envs/develop.tfvars -auto-approve
```

### 3. Iniciar Replicação DMS
```bash
./modules/dms-serverless/start_replication.sh dev
```

## 📊 Pipeline de Dados

### 1. Ingestão
- **DMS**: Replica dados do PostgreSQL para S3 (full-load + CDC)
- **Debezium**: Captura mudanças em tempo real via Kafka

### 2. Processamento
- **Glue ETL**: Transforma dados raw em dimensões e fatos
- **S3 Tables**: Armazena dados em formato Iceberg
- **Step Functions**: Orquestra pipeline ETL

### 3. Consumo
- **OpenSearch**: Analytics e busca em tempo real
- **Lambda + DuckDB**: Queries analíticas
- **S3 Tables**: Consultas SQL diretas

## 🔄 Configuração CDC

### RDS PostgreSQL
```sql
-- Configurações necessárias no Parameter Group
rds.logical_replication = 1
max_replication_slots = 10
max_wal_senders = 10
```

### Debezium + Kafka
```bash
cd debezium
docker-compose up -d
```

### Configurar Conectores
```bash
# Conector PostgreSQL para web_events
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @connect-configs/postgres.json

# Verificar status
curl http://localhost:8083/connectors/postgres-connector-ecommerce-final/status
```

## 🧪 S3 Tables Iceberg

### Configurar Connector
1. Build do connector oficial:
```bash
./debezium/build-iceberg-s3-connect.sh
```

2. Configurar JARs:
```bash
# JARs Debezium (Avro/Schema Registry)
cp jars/debezium/* kafka-connect-debezium/

# JARs do Iceberg
cp /iceberg/kafka-connect/kafka-connect-runtime/build/distributions/* kafka-connect-confluent
```


### JARs Incluídos

#### Debezium (`jars/debezium/`)
- `kafka-avro-serializer-8.0.0.jar`
- `kafka-connect-avro-converter-8.0.0.jar`
- `kafka-schema-registry-client-8.0.0.jar`

#### Spark Streaming (`jars/spark-streaming/`)
- `opensearch-spark-30_2.12-1.3.0.jar`
- `spark-sql-kafka-0-10_2.12-3.3.4.jar`
- `spark-avro_2.12-3.3.4.jar`
- `kafka-clients-3.5.2.jar`

## 🔍 OpenSearch

### Deploy
```bash
cd opensearch
docker-compose up -d
```

### Acesso
- **URL**: http://localhost:5601
- **Usuário**: admin
- **Senha**: admin

## 📊 Metabase

### Deploy
```bash
cd metabase
docker-compose up -d
```

### Acesso
- **URL**: http://localhost:3000
- **Configuração**: Primeira execução requer setup inicial
- **Banco**: PostgreSQL interno para metadados

## 📝 Scripts Disponíveis

### Glue ETL
- `datahandson-dataopsfinops-amazonsales-dw-table-stg-s3tables.py` - Staging
- `datahandson-dataopsfinops-amazonsales-dw-dim-*.py` - Dimensões
- `datahandson-dataopsfinops-amazonsales-dw-fact-*.py` - Fatos
- `*-gdq.py` - Data Quality

### Spark Streaming
- `datahandson-dataopsfinops-webevents-streaming-kafka-opensearch.py` - Streaming Kafka → OpenSearch

### Lambda
- `lambda_handler.py` - Queries analíticas com DuckDB
- `build_and_push.sh` - Build e deploy container ECR
- `Dockerfile` - Container Lambda

### Utilitários
- `script-insert-postgres-webfake-events.py` - Geração de dados fake
- `ec2_bootstrap.sh` - Inicialização instâncias EC2

## 🛠️ Monitoramento

### DMS
```bash
./modules/dms-serverless/monitor_replication.sh dev
```

### Step Functions
- Console AWS Step Functions
- CloudWatch Logs

### Glue Jobs
- Console AWS Glue
- CloudWatch Metrics

### Kafka + Debezium
```bash
# Status conectores
curl http://localhost:8083/connectors

# Logs
docker-compose logs -f connect
```

## 🔧 Troubleshooting

### Debezium
```bash
# Verificar conectores
curl http://localhost:8083/connectors

# Status detalhado
curl http://localhost:8083/connectors/postgres-connector-ecommerce-final/status

# Reiniciar conector
curl -X POST http://localhost:8083/connectors/postgres-connector-ecommerce-final/restart

# Logs do Kafka Connect
docker-compose logs -f connect
```

### Kafka Topics
```bash
# Listar tópics
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Consumir mensagens
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic ecommercefinal.public.web_events \
  --from-beginning
```

### Glue Jobs
```bash
# Logs CloudWatch
aws logs describe-log-groups --log-group-name-prefix "/aws-glue/jobs"

# Status job
aws glue get-job-run --job-name <job-name> --run-id <run-id>
```

## 📋 Variáveis de Ambiente

### Desenvolvimento (`envs/develop.tfvars`)
```hcl
environment = "dev"
region = "us-east-2"
s3_bucket_raw = "cjmm-mds-lake-raw"
s3_bucket_scripts = "cjmm-mds-lake-configs"
s3_bucket_curated = "cjmm-mds-lake-curated"
```

## 🔐 Segurança

- IAM Roles com princípio de menor privilégio
- Security Groups restritivos
- VPC Endpoints para comunicação privada
- Criptografia em trânsito e repouso

## 🔄 CI/CD com GitHub Actions

### Pipeline Terraform (`github-actions/terraform.yml`)
- **Triggers**: Pull requests e pushes para `develop` e `main`
- **Ambientes**: Automático baseado na branch
  - `develop` → ambiente `dev`
  - `main` → ambiente `prod`
- **Steps**:
  - Terraform fmt, validate e plan
  - Apply automático em push para branches principais
  - Upload de artifacts do plan em PRs

### Configuração
```yaml
# Secrets necessários no GitHub:
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

### Uso
1. **Pull Request**: Executa plan e valida código
2. **Merge**: Aplica mudanças automaticamente
3. **Artifacts**: Plan disponível para review

## 🎯 Casos de Uso

### 1. E-commerce Analytics
- Análise de vendas por categoria
- Ratings de produtos
- Comportamento de usuários

### 2. Real-time Streaming
- Eventos web em tempo real
- Processamento Kafka → OpenSearch
- Dashboards interativos

### 3. Data Quality
- Validação com Great Expectations
- Monitoramento de qualidade
- Alertas automáticos

## 📚 Tecnologias

- **AWS**: RDS, DMS, Glue, Step Functions, Lambda, S3, EventBridge
- **Terraform**: Infraestrutura como código
- **GitHub Actions**: CI/CD pipeline
- **Apache Kafka**: Streaming de dados
- **Debezium**: Change Data Capture
- **Apache Iceberg**: Table format para Data Lake
- **OpenSearch**: Search e analytics
- **Metabase**: Business Intelligence
- **DuckDB**: Analytics engine
- **Docker**: Containerização
