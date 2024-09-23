from pydantic import BaseModel
from typing import Optional

class VideoCreate(BaseModel):
    name: str
    size: int
    path: Optional[str] = None

class VideoSearch(BaseModel):
    name: Optional[str] = None
    size: Optional[int] = None

class VideoResponse(BaseModel):
    id: int
    name: str
    size: int
    path: str
    converted: str

    class Config:
        orm_mode = True
