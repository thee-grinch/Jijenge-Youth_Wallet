from pydantic import BaseModel
from typing import List, Optional

#generate a pydantic model for the contribution
class ContributionSchema(BaseModel):
    # user_id: int
    amount: int
    date: Optional[str]