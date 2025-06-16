from typing import List, Optional
from pydantic import BaseModel


class Request(BaseModel):
    id: Optional[str] = None
    instagram: str
    content: str = None
    assets: Optional[List[str]] = []
