import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base, get_db
from main import app
import tasks

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Создаем тестовую категорию, чтобы заметки могли создаваться
    from models.category import Category
    db.add(Category(id=1, name="Тестовая категория"))
    db.commit()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    
    # Мокаем Celery, чтобы тесты не требовали запущенного Redis
    class MockTask:
        def delay(self, *args, **kwargs):
            pass
    import routers.notes
    tasks.send_note_notification = MockTask()
    routers.notes.send_note_notification = MockTask()

    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()