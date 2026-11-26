import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from core.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default=UserRole.USER.value)
    
    # Связь один ко многим: у пользователя много заметок
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="owner")