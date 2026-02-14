from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from services.fetcher import fetch_uuid
from services.ai_enrichment import enrich_uuid
from services.storage import store_result

from services.notifier import send_notification

app = FastAPI()

class PipelineRequest(BaseModel):
    email: str
    source: str

@app.post("/pipeline")
def run_pipeline(request: PipelineRequest):
    items = []
    errors = []

    for i in range(3):
        try:
            uuid = fetch_uuid()
        except Exception as e:
            errors.append(f"Fetch error: {str(e)}")
            continue

        try:
            analysis, sentiment = enrich_uuid(uuid)
        except Exception as e:
            errors.append(f"AI error: {str(e)}")
            continue

        try:
            timestamp = datetime.utcnow().isoformat()
            store_result(uuid, analysis, sentiment, timestamp, request.source)
            stored = True
        except Exception as e:
            stored = False
            errors.append(f"Storage error: {str(e)}")

        items.append({
            "original": uuid,
            "analysis": analysis,
            "sentiment": sentiment,
            "stored": stored,
            "timestamp": timestamp
        })

    try:
        send_notification(request.email)
        notification_sent = True
    except Exception as e:
        notification_sent = False
        errors.append(f"Notification error: {str(e)}")

    return {
        "items": items,
        "notificationSent": notification_sent,
        "processedAt": datetime.utcnow().isoformat(),
        "errors": errors
    }
