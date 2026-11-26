from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    content: str = Field(default="")
    category_id: int

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    category_id: int
    
    class Config:
        from_attributes = True