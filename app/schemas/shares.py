from pydantic import BaseModel
from typing import List, Optional

#generate a pydantic model for the share
class ShareSchema(BaseModel):
    amount: int
    date: Optional[str]