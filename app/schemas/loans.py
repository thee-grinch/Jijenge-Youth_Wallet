from pydantic import BaseModel


class create_loan(BaseModel):
    """this model describes the necessary fields for creating loans"""
    user_id: int
    amount: int
    loan_type_id: int
    
