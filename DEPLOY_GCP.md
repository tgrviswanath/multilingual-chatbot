# GCP Deployment Guide — Project 08 Multilingual FAQ Chatbot

---

## GCP Services for Multilingual Chatbot

### 1. Ready-to-Use AI (No Model Needed)

| Service                              | What it does                                                                 | When to use                                        |
|--------------------------------------|------------------------------------------------------------------------------|----------------------------------------------------|
| **Dialogflow CX**                    | Intent detection and conversation flow for FAQ chatbot                       | Replace your TF-IDF + LinearSVC intent classifier  |
| **Cloud Translation API**            | Translate 100+ languages — replace your MarianMT translation pipeline        | Replace Helsinki-NLP MarianMT models               |
| **Vertex AI Gemini**                 | Gemini Pro for multilingual FAQ responses without intent classification      | When you need flexible, open-ended responses       |
| **Cloud Natural Language API**       | Detect language from user messages                                           | Replace your langdetect pipeline                   |

> **Dialogflow CX + Cloud Translation API** together replace your entire langdetect + MarianMT + TF-IDF pipeline with managed GCP services.

### 2. Host Your Own Model (Keep Current Stack)

| Service                    | What it does                                                        | When to use                                           |
|----------------------------|---------------------------------------------------------------------|-------------------------------------------------------|
| **Cloud Run**              | Run backend + nlp-service containers — serverless, scales to zero   | Best match for your current microservice architecture |
| **Artifact Registry**      | Store your Docker images                                            | Used with Cloud Run or GKE                            |

### 3. Frontend Hosting

| Service                    | What it does                                                              |
|----------------------------|---------------------------------------------------------------------------|
| **Firebase Hosting**       | Host your React chat frontend — free tier, auto CI/CD from GitHub         |

### 4. Supporting Services

| Service                        | Purpose                                                                   |
|--------------------------------|---------------------------------------------------------------------------|
| **Cloud Memorystore (Redis)**  | Cache FAQ responses and translation results                               |
| **Secret Manager**             | Store API keys and connection strings instead of .env files               |
| **Cloud Monitoring + Logging** | Track intent accuracy, language distribution, response latency            |

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Firebase Hosting — React Chat Frontend                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│  Cloud Run — Backend (FastAPI :8000)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ Internal HTTPS
        ┌──────────────┴──────────────┐
        │ Option A                    │ Option B
        ▼                             ▼
┌───────────────────┐    ┌────────────────────────────────────┐
│ Cloud Run         │    │ Dialogflow CX                      │
│ NLP Service :8001 │    │ + Cloud Translation API            │
│ langdetect+MarianMT│   │ No model download needed           │
└───────────────────┘    └────────────────────────────────────┘
```

---

## Prerequisites

```bash
gcloud auth login
gcloud projects create chatbot-project --name="Multilingual Chatbot"
gcloud config set project chatbot-project
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  secretmanager.googleapis.com translate.googleapis.com \
  dialogflow.googleapis.com language.googleapis.com cloudbuild.googleapis.com
```

---

## Step 1 — Create Artifact Registry and Push Images

```bash
GCP_REGION=europe-west2
gcloud artifacts repositories create chatbot-repo \
  --repository-format=docker --location=$GCP_REGION
gcloud auth configure-docker $GCP_REGION-docker.pkg.dev
AR=$GCP_REGION-docker.pkg.dev/chatbot-project/chatbot-repo
docker build -f docker/Dockerfile.nlp-service -t $AR/nlp-service:latest ./nlp-service
docker push $AR/nlp-service:latest
docker build -f docker/Dockerfile.backend -t $AR/backend:latest ./backend
docker push $AR/backend:latest
```

---

## Step 2 — Deploy to Cloud Run

```bash
gcloud run deploy nlp-service \
  --image $AR/nlp-service:latest --region $GCP_REGION \
  --port 8001 --no-allow-unauthenticated \
  --min-instances 1 --max-instances 3 --memory 2Gi --cpu 1

NLP_URL=$(gcloud run services describe nlp-service --region $GCP_REGION --format "value(status.url)")

gcloud run deploy backend \
  --image $AR/backend:latest --region $GCP_REGION \
  --port 8000 --allow-unauthenticated \
  --min-instances 1 --max-instances 5 --memory 1Gi --cpu 1 \
  --set-env-vars NLP_SERVICE_URL=$NLP_URL
```

---

## Option B — Use Cloud Translation API

```python
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def process_message(text: str) -> dict:
    detection = translate_client.detect_language(text)
    source_lang = detection["language"]

    english_text = text
    if source_lang != "en":
        result = translate_client.translate(text, target_language="en")
        english_text = result["translatedText"]

    return {"original": text, "english": english_text, "detected_language": source_lang}
```

Add to requirements.txt: `google-cloud-translate>=3.12.0`

---

## Estimated Monthly Cost

| Service                    | Tier                  | Est. Cost          |
|----------------------------|-----------------------|--------------------|
| Cloud Run (backend)        | 1 vCPU / 1 GB         | ~$10–15/month      |
| Cloud Run (nlp-service)    | 1 vCPU / 2 GB         | ~$12–18/month      |
| Artifact Registry          | Storage               | ~$1–2/month        |
| Firebase Hosting           | Free tier             | $0                 |
| Cloud Translation API      | Pay per character     | ~$5–10/month       |
| **Total (Option A)**       |                       | **~$23–35/month**  |
| **Total (Option B)**       |                       | **~$16–27/month**  |

For exact estimates → https://cloud.google.com/products/calculator

---

## Teardown

```bash
gcloud run services delete backend --region $GCP_REGION --quiet
gcloud run services delete nlp-service --region $GCP_REGION --quiet
gcloud artifacts repositories delete chatbot-repo --location=$GCP_REGION --quiet
gcloud projects delete chatbot-project
```
