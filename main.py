import random
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(
    title="Cloud AI Cyber Defense SOC",
    description="Платформа обнаружения и предотвращения кибератак в облачной среде с использованием ИИ",
    version="1.0.0",
)

# Настройка шаблонизатора
templates = Jinja2Templates(directory="templates")


# Модель данных для входящего запроса на анализ логов/трафика
class CloudLogPayload(BaseModel):
    source_ip: str = Field(..., example="192.168.1.50", description="IP-адрес источника")
    cloud_region: str = Field(..., example="us-east-1", description="Регион облачной инфраструктуры")
    request_rate: int = Field(..., example=1200, description="Количество запросов в секунду")
    payload_signature: str = Field(..., example="SELECT * FROM users...", description="Сигнатура запроса")


# Имитация базы данных логов в памяти
RECENT_ALERTS = [
    {
        "id": "INC-8832",
        "timestamp": "2026-06-06 14:22:10",
        "type": "DDoS / Volumetric",
        "severity": "Critical",
        "status": "Blocked by AI",
        "source": "45.154.255.88"
    },
    {
        "id": "INC-8831",
        "timestamp": "2026-06-06 14:19:05",
        "type": "SQL Injection Attempt",
        "severity": "High",
        "status": "Mitigated",
        "source": "185.220.101.5"
    },
    {
        "id": "INC-8830",
        "timestamp": "2026-06-06 14:15:40",
        "type": "Anomalous IAM Privilege Escalation",
        "severity": "Medium",
        "status": "Investigating",
        "source": "AWS-IAM-Role-Worker-Dev"
    }
]


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Рендеринг главной страницы SOC-панели"""
    # Исправлено: request передан первым позиционным аргументом без ключевого слова
    return templates.TemplateResponse(
        request,
        "index.html", 
        {"alerts": RECENT_ALERTS}
    )


@app.post("/api/v1/analyze")
async def analyze_traffic(payload: CloudLogPayload):
    """Эндпоинт ИИ-модуля для анализа облачных аномалий в реальном времени"""
    
    # Имитация логики ИИ-модели (например, Isolation Forest / Autoencoder / Neural Net)
    risk_score = random.uniform(0.1, 0.99)
    
    # Эвристика для демонстрации
    is_attack = risk_score > 0.75 or "SELECT" in payload.payload_signature.upper() or payload.request_rate > 1000
    
    threat_type = "Normal Traffic"
    action_taken = "Allowed"
    
    if is_attack:
        if payload.request_rate > 1000:
            threat_type = "DDoS / High-Frequency Flooding"
        elif "SELECT" in payload.payload_signature.upper():
            threat_type = "SQL Injection / Data Exfiltration"
        else:
            threat_type = "Zero-Day Behavioral Anomaly"
        action_taken = "Automated Block & Sandbox Isolation"
        
    result = {
        "status": "success",
        "risk_score": round(risk_score, 4),
        "anomaly_detected": is_attack,
        "classification": threat_type,
        "recommended_action": action_taken,
        "region": payload.cloud_region
    }
    
    if is_attack:
        RECENT_ALERTS.insert(0, {
            "id": f"INC-{random.randint(9000, 9999)}",
            "timestamp": "Just now",
            "type": threat_type,
            "severity": "Critical" if risk_score > 0.85 else "High",
            "status": "Mitigated by AI",
            "source": payload.source_ip
        })
        if len(RECENT_ALERTS) > 10:
            RECENT_ALERTS.pop()
            
    return result


if __name__ == "__main__":
    # Запуск сервера
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
