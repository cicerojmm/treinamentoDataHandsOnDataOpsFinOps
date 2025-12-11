# treinamentoDataHandsOnDataOpsFinOps
Treinamento sobre DataOps e FinOps

## Arquitetura

### Componentes Principais
- **EMR Serverless**: Processamento Spark com arquitetura ARM64 (Graviton)
- **Airflow**: Orquestração de pipelines
- **Glue Data Quality**: Monitoramento de qualidade de dados
- **EventBridge + Lambda**: Alertas automatizados
- **S3**: Data Lake (raw, processed, scripts)

### Otimizações FinOps
- **Graviton (ARM64)**: Redução de custos em até 20% no EMR Serverless
- **Auto-scaling**: Configuração automática de recursos
- **Idle timeout**: Desligamento automático após 5 minutos
- **EC2 Scheduler**: Start/stop automático de instâncias

### Monitoramento
- **Data Quality**: Alertas via Discord para falhas
- **Health Check**: Monitoramento do Airflow
- **CloudWatch**: Logs centralizados

## Deploy
```bash
cd terraform/infra
terraform init
terraform plan
terraform apply
```
