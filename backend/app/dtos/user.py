from pydantic import BaseModel,EmailStr
from datetime import datetime
class CreateUser(BaseModel):
    user_name:str
    email:EmailStr
    password:str

class ResponseUser(BaseModel):
    id:int
    user_name:str
    email:EmailStr
    created_at:datetime

class LoginCreate(BaseModel):
    identifier:str
    password:str
