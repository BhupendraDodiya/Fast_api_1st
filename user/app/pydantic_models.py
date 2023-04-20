from pydantic import BaseModel

class Person(BaseModel):
    name:str
    phone:int
    email:str
    password:str

class Loginuser(BaseModel):
    phone:str
    password:str

class Token(BaseModel):
    access_token : str
    token_type : str = 'bearer'

class One(BaseModel):
    id:int

class Delete(BaseModel):
    id : int

class Update(BaseModel):
    id:int
    name:str
    phone:int
    email:str
    password:str