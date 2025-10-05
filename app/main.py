# app/main.py
from fastapi import FastAPI
from transformers import pipeline
import os

# Создаём FastAPI-приложение — ОБЯЗАТЕЛЬНО с именем "app"
app = FastAPI(
    title="Sentiment Analysis API",
    description="Scalable ML service using Hugging Face + FastAPI + Kubernetes",
    version="1.0"
)

# Загружаем модель один раз при старте контейнера
print("Loading model...")
model_path = "/app/model"
if not os.path.exists(model_path):
    raise RuntimeError(f"Model not found at {model_path}! Did you copy it in Dockerfile?")

model = pipeline("sentiment-analysis", model=model_path)
print("Model loaded successfully!")

@app.get("/predict")
def predict(text: str):
    """
    Predict sentiment of input text.
    Example: ?text=I love machine learning!
    """
    if not text.strip():
        return {"error": "Text cannot be empty"}
    
    result = model(text)[0]
    return {
        "text": text,
        "sentiment": result["label"],
        "confidence": round(float(result["score"]), 4)
    }

@app.get("/health")
def health():
    """Health check for Kubernetes liveness/readiness probes"""
    return {"status": "healthy", "model_loaded": True}