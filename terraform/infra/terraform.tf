terraform {
  backend "s3" {
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
  default_tags {
    tags = {
      "Application"    = "data-handson-dataops-finops"
      "Project"        = "data-handson-mds"
      "Environment"    = var.environment
      "Owner"          = "DataOps Team"
      "CostCenter"     = "DataEngineering"
      "ManagedBy"      = "Terraform"
      "awsApplication" = "arn:aws:resource-groups:us-east-2:296735965303:group/data-handson-dataops-finops/059dqo3tmuo2917tzbaz65g71w"
    }
  }
}
