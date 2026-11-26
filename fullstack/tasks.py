import time
from celery_app import celery_app

@celery_app.task
def send_note_notification(title: str, email: str):
    time.sleep(2)  # Имитация долгой отправки email
    print(f"Уведомление о заметке '{title}' отправлено на {email}")
    return {"status": "sent", "email": email, "title": title}