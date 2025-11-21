from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Link(SQLModel, table=True):
    __tablename__ = "links"

    id: Optional[int] = Field(default=None, primary_key=True)
    short_code: str = Field(index=True, unique=True)
    original_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    clicks: int = Field(default=0)


