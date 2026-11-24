
from fastapi import FastAPI

app = FastAPI(
    title="Wifi-AI Secure API",
    description="AI-assisted Wi-Fi attack detection system",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Wifi-AI Secure",
        "version": "0.1.0",
        "status": "running",
        "mode": "development",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "wifi-ai-secure-api",
    }
