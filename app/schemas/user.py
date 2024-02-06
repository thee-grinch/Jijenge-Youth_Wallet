from pydantic import BaseModel

class CreateUser(BaseModel):
    """this is a pydantic model for creating a new user"""
    name: str
    password: str
    first_name: str
    last_name: str
    email: str