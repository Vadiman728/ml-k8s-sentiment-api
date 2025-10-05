# Скрипт загрузки модели

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
print("Downloading model...")
classifier = pipeline("sentiment-analysis", model=model_name)
classifier.save_pretrained("./model")
print("Model saved to ./model")
