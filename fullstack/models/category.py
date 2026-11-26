from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    
    # Связь один ко многим: в категории много заметок
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="category")