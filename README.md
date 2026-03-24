# Project 08 - Multilingual FAQ Chatbot

Microservice NLP chatbot that detects the user's language, classifies intent, generates a response, and translates it back — supporting 10+ languages via Helsinki-NLP MarianMT models.

## Architecture

```
Frontend :3000  →  Backend :8000  →  NLP Service :8001
  React/MUI        FastAPI/httpx      langdetect + TF-IDF + MarianMT
```

## Flow

```
User message (any language)
  → langdetect detects language
  → MarianMT translates to English (if needed)
  → TF-IDF + LinearSVC classifies intent
  → FAQ response selected
  → MarianMT translates response back to user language
  → Response displayed in chat UI
```

## Local Run

```bash
# Terminal 1 - NLP Service
cd nlp-service && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
python train.py          # trains intent classifier (~2 seconds)
uvicorn app.main:app --reload --port 8001

# Terminal 2 - Backend
cd backend && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 3 - Frontend
cd frontend && npm install && npm start
```

## Docker

```bash
docker-compose up --build
```

## Stack

| Layer | Tools |
|-------|-------|
| NLP Service | langdetect, Helsinki-NLP MarianMT, TF-IDF + LinearSVC |
| Backend | FastAPI, httpx |
| Frontend | React, MUI (chat bubbles, chips, switch) |

## Supported Languages

English, French, Spanish, German, Italian, Portuguese, Dutch, Russian, Chinese, Arabic

## Intents

greeting, farewell, hours, pricing, refund, contact, account, shipping, thanks, unknown
