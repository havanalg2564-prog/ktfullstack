from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user, require_role
from models.user import User, UserRole
from schemas.note import NoteCreate, NoteResponse
from services import note_service
from tasks import send_note_notification

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse)
def create_note(
    note_data: NoteCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = note_service.create_note(note_data, current_user.id, db)
    # Отправляем задачу в очередь Celery
    send_note_notification.delay(note.title, current_user.email)
    return note

@router.get("/", response_model=list[NoteResponse])
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return note_service.get_user_notes(current_user.id, db)

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    # RBAC: доступ только для админов
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    note_service.delete_note(note_id, db)
    return {"message": "Заметка успешно удалена"}