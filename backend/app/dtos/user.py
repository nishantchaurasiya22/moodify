from pydantic import BaseModel,EmailStr,Field

class CreateUser(BaseModel):
    user_name:str=Field(min_length=5,max_length=100)
    email:EmailStr=Field(min_length=5,max_length=255)
    password:str=Field(min_length=8,max_length=100)

class ResponseUser(BaseModel):
    id:int
    user_name:str
    email:EmailStr

class CreateLogin(BaseModel):
    identifier:str=Field(min_length=5,max_length=255)
    password:str=Field(min_length=8,max_length=100)

