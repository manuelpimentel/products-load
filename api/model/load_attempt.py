from typing import List, Optional
from pydantic import BaseModel


class LoadAttempt(BaseModel):
    id: Optional[str] = None
    instagram: str = None
    content: str = None
    assets: Optional[List[str]] = []

    def is_valid(self):
        if self.instagram and self.content:
            return True
        elif not self.instagram and "instagram:" not in self.content:
            return False
        else:
            return True
