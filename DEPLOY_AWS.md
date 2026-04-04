# AWS Deployment Guide — Project 08 Multilingual FAQ Chatbot

---

## AWS Services for Multilingual Chatbot

### 1. Ready-to-Use AI (No Model Needed)

| Service                    | What it does                                                                 | When to use                                        |
|----------------------------|------------------------------------------------------------------------------|----------------------------------------------------|
| **Amazon Lex**             | Intent detection and slot filling for FAQ chatbot                            | Replace your TF-IDF + LinearSVC intent classifier  |
| **Amazon Translate**       | Translate 75+ languages — replace your MarianMT translation pipeline         | Replace Helsinki-NLP MarianMT models               |
| **Amazon Bedrock**         | Claude/Titan for multilingual FAQ responses without intent classification    | When you need flexible, open-ended responses       |
| **Amazon Comprehend**      | Detect dominant language from user messages                                  | Replace your langdetect pipeline                   |

> **Amazon Lex + Amazon Translate + Amazon Comprehend** together replace your entire langdetect + MarianMT + TF-IDF pipeline with managed AWS services.

### 2. Host Your Own Model (Keep Current Stack)

| Service                    | What it does                                                        | When to use                                           |
|----------------------------|---------------------------------------------------------------------|-------------------------------------------------------|
| **AWS App Runner**         | Run backend container — simplest, no VPC or cluster needed          | Quickest path to production                           |
| **Amazon ECS Fargate**     | Run backend + nlp-service containers in a private VPC               | Best match for your current microservice architecture |
| **Amazon ECR**             | Store your Docker images                                            | Used with App Runner, ECS, or EKS                     |

### 3. Frontend Hosting

| Service               | What it does                                                                  |
|-----------------------|-------------------------------------------------------------------------------|
| **Amazon S3**         | Host your React chat frontend as a static website                             |
| **Amazon CloudFront** | CDN in front of S3 — HTTPS, low latency globally                              |

### 4. Supporting Services

| Service                  | Purpose                                                                   |
|--------------------------|---------------------------------------------------------------------------|
| **Amazon ElastiCache**   | Cache FAQ responses and translation results                               |
| **AWS Secrets Manager**  | Store API keys and connection strings instead of .env files               |
| **Amazon CloudWatch**    | Track intent accuracy, language distribution, response latency            |

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  S3 + CloudFront — React Chat Frontend                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│  AWS App Runner / ECS Fargate — Backend (FastAPI :8000)     │
└──────────────────────┬──────────────────────────────────────┘
                       │ Internal
        ┌──────────────┴──────────────┐
        │ Option A                    │ Option B
        ▼                             ▼
┌───────────────────┐    ┌────────────────────────────────────┐
│ ECS Fargate       │    │ Amazon Lex + Amazon Translate      │
│ NLP Service :8001 │    │ + Amazon Comprehend                │
│ langdetect+MarianMT│   │ No model download needed           │
└───────────────────┘    └────────────────────────────────────┘
```

---

## Prerequisites

```bash
aws configure
AWS_REGION=eu-west-2
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
```

---

## Step 1 — Create ECR and Push Images

```bash
aws ecr create-repository --repository-name chatbot/nlp-service --region $AWS_REGION
aws ecr create-repository --repository-name chatbot/backend --region $AWS_REGION
ECR=$AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR
docker build -f docker/Dockerfile.nlp-service -t $ECR/chatbot/nlp-service:latest ./nlp-service
docker push $ECR/chatbot/nlp-service:latest
docker build -f docker/Dockerfile.backend -t $ECR/chatbot/backend:latest ./backend
docker push $ECR/chatbot/backend:latest
```

---

## Step 2 — Deploy with App Runner

```bash
aws apprunner create-service \
  --service-name chatbot-backend \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "'$ECR'/chatbot/backend:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "NLP_SERVICE_URL": "http://nlp-service:8001"
        }
      }
    }
  }' \
  --instance-configuration '{"Cpu": "1 vCPU", "Memory": "2 GB"}' \
  --region $AWS_REGION
```

---

## Option B — Use Amazon Translate + Comprehend

```python
import boto3

translate = boto3.client("translate", region_name="eu-west-2")
comprehend = boto3.client("comprehend", region_name="eu-west-2")

def process_message(text: str) -> dict:
    # Detect language
    lang_result = comprehend.detect_dominant_language(Text=text)
    source_lang = lang_result["Languages"][0]["LanguageCode"]

    # Translate to English if needed
    english_text = text
    if source_lang != "en":
        translated = translate.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode="en"
        )
        english_text = translated["TranslatedText"]

    return {"original": text, "english": english_text, "detected_language": source_lang}
```

---

## Estimated Monthly Cost

| Service                    | Tier              | Est. Cost          |
|----------------------------|-------------------|--------------------|
| App Runner (backend)       | 1 vCPU / 2 GB     | ~$20–25/month      |
| App Runner (nlp-service)   | 1 vCPU / 2 GB     | ~$20–25/month      |
| ECR + S3 + CloudFront      | Standard          | ~$3–7/month        |
| Amazon Translate           | Pay per character | ~$5–10/month       |
| **Total (Option A)**       |                   | **~$43–57/month**  |
| **Total (Option B)**       |                   | **~$28–42/month**  |

For exact estimates → https://calculator.aws

---

## Teardown

```bash
aws ecr delete-repository --repository-name chatbot/backend --force
aws ecr delete-repository --repository-name chatbot/nlp-service --force
```
