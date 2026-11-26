import os

from celery import Celery

# Настройка Celery с использованием Redis в качестве брокера.
# URL можно переопределить через переменную окружения (например, для Docker Compose).
BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=BROKER_URL,
)

# Если Redis не используется (например, деплой на Railway без Redis),
# задачи выполняются синхронно в том же процессе — отдельный worker не нужен.
if os.getenv("CELERY_TASK_ALWAYS_EAGER", "").lower() in ("1", "true", "yes"):
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
