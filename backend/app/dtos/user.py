from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class CreateUser(BaseModel):
    user_name:str=Field(min_length=5,max_length=100)
    email:str=Field(min_length=5,max_length=255)
    password:str=Field(min_length=8,max_length=100)

class ResponseUser(BaseModel):
    id:int
    user_name:str
    email:EmailStr
    created_at:datetime
    updated_at:datetime

class LoginUser(BaseModel):
    identifier:str=Field(min_length=5,max_length=255)
    password:str=Field(min_length=8,max_length=100)