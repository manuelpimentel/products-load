from typing import List, Optional
from pydantic import BaseModel


class Load(BaseModel):
    id: Optional[str] = None
    instagram: str
    content: str = None
    assets: Optional[List[str]] = []
