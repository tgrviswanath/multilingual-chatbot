# Azure Deployment Guide — Project 08 Multilingual FAQ Chatbot

---

## Azure Services for Multilingual Chatbot

### 1. Ready-to-Use AI (No Model Needed)

| Service                              | What it does                                                                 | When to use                                        |
|--------------------------------------|------------------------------------------------------------------------------|----------------------------------------------------|
| **Azure AI Language — CLU**          | Conversational Language Understanding — intent + entity detection            | Replace your TF-IDF + LinearSVC intent classifier  |
| **Azure AI Translator**              | Translate 100+ languages — replace your MarianMT translation pipeline        | Replace Helsinki-NLP MarianMT models               |
| **Azure OpenAI Service**             | GPT-4 for multilingual FAQ responses without intent classification           | When you need flexible, open-ended responses       |
| **Azure Bot Service**                | Full chatbot framework with channel integrations (Teams, Slack, Web)         | When you need a production chatbot platform        |

> **Azure AI Language CLU + Azure AI Translator** together replace your entire langdetect + MarianMT + TF-IDF pipeline with managed APIs.

### 2. Host Your Own Model (Keep Current Stack)

| Service                        | What it does                                                        | When to use                                           |
|--------------------------------|---------------------------------------------------------------------|-------------------------------------------------------|
| **Azure Container Apps**       | Run your 3 Docker containers (frontend, backend, nlp-service)       | Best match for your current microservice architecture |
| **Azure Container Registry**   | Store your Docker images                                            | Used with Container Apps or AKS                       |

### 3. Frontend Hosting

| Service                   | What it does                                                               |
|---------------------------|----------------------------------------------------------------------------|
| **Azure Static Web Apps** | Host your React chat frontend — free tier available                        |

### 4. Supporting Services

| Service                       | Purpose                                                                  |
|-------------------------------|--------------------------------------------------------------------------|
| **Azure Cache for Redis**     | Cache FAQ responses and translation results                              |
| **Azure Key Vault**           | Store API keys and connection strings instead of .env files              |
| **Azure Monitor + App Insights** | Track intent accuracy, language distribution, response latency        |

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Azure Static Web Apps — React Chat Frontend                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│  Azure Container Apps — Backend (FastAPI :8000)             │
└──────────────────────┬──────────────────────────────────────┘
                       │ Internal
        ┌──────────────┴──────────────┐
        │ Option A                    │ Option B
        ▼                             ▼
┌───────────────────┐    ┌────────────────────────────────────┐
│ Container Apps    │    │ Azure AI Language CLU              │
│ NLP Service :8001 │    │ + Azure AI Translator              │
│ langdetect+MarianMT│   │ No model download needed           │
└───────────────────┘    └────────────────────────────────────┘
```

---

## Prerequisites

```bash
az login
az group create --name rg-multilingual-chatbot --location uksouth
az extension add --name containerapp --upgrade
```

---

## Step 1 — Create Container Registry and Push Images

```bash
az acr create --resource-group rg-multilingual-chatbot --name multilingualchatbotacr --sku Basic --admin-enabled true
az acr login --name multilingualchatbotacr
ACR=multilingualchatbotacr.azurecr.io
docker build -f docker/Dockerfile.nlp-service -t $ACR/nlp-service:latest ./nlp-service
docker push $ACR/nlp-service:latest
docker build -f docker/Dockerfile.backend -t $ACR/backend:latest ./backend
docker push $ACR/backend:latest
```

---

## Step 2 — Deploy Container Apps

```bash
az containerapp env create --name chatbot-env --resource-group rg-multilingual-chatbot --location uksouth

az containerapp create \
  --name nlp-service --resource-group rg-multilingual-chatbot \
  --environment chatbot-env --image $ACR/nlp-service:latest \
  --registry-server $ACR --target-port 8001 --ingress internal \
  --min-replicas 1 --max-replicas 3 --cpu 1 --memory 2.0Gi

az containerapp create \
  --name backend --resource-group rg-multilingual-chatbot \
  --environment chatbot-env --image $ACR/backend:latest \
  --registry-server $ACR --target-port 8000 --ingress external \
  --min-replicas 1 --max-replicas 5 --cpu 0.5 --memory 1.0Gi \
  --env-vars NLP_SERVICE_URL=http://nlp-service:8001
```

---

## Option B — Use Azure AI Language CLU + Translator

```bash
# Create Translator resource
az cognitiveservices account create \
  --name chatbot-translator \
  --resource-group rg-multilingual-chatbot \
  --kind TextTranslation --sku S1 --location uksouth --yes

# Create Language resource for CLU
az cognitiveservices account create \
  --name chatbot-language \
  --resource-group rg-multilingual-chatbot \
  --kind TextAnalytics --sku S --location uksouth --yes
```

```python
import requests

def translate_to_english(text: str, source_lang: str) -> str:
    url = "https://api.cognitive.microsofttranslator.com/translate"
    params = {"api-version": "3.0", "from": source_lang, "to": "en"}
    headers = {"Ocp-Apim-Subscription-Key": os.getenv("AZURE_TRANSLATOR_KEY")}
    body = [{"text": text}]
    result = requests.post(url, params=params, headers=headers, json=body)
    return result.json()[0]["translations"][0]["text"]
```

---

## Estimated Monthly Cost

| Service                  | Tier      | Est. Cost         |
|--------------------------|-----------|-------------------|
| Container Apps (backend) | 0.5 vCPU  | ~$10–15/month     |
| Container Apps (nlp-svc) | 1 vCPU    | ~$15–20/month     |
| Container Registry       | Basic     | ~$5/month         |
| Static Web Apps          | Free      | $0                |
| Azure AI Translator      | S1 tier   | Pay per character |
| **Total (Option A)**     |           | **~$30–40/month** |
| **Total (Option B)**     |           | **~$15–20/month** |

For exact estimates → https://calculator.azure.com

---

## Teardown

```bash
az group delete --name rg-multilingual-chatbot --yes --no-wait
```
