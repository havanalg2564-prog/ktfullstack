from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.note import Note
from schemas.note import NoteCreate

def create_note(note_data: NoteCreate, owner_id: int, db: Session) -> Note:
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        category_id=note_data.category_id,
        owner_id=owner_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_user_notes(owner_id: int, db: Session) -> list[Note]:
    return db.query(Note).filter(Note.owner_id == owner_id).all()

def delete_note(note_id: int, db: Session):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    
    db.delete(note)
    db.commit()