from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Link(SQLModel, table=True):
    __tablename__ = "links"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    target_url: str = Field(index=True) 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    clicks: int = Field(default=0)