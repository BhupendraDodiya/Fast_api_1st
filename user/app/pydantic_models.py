from pydantic import BaseModel

class Person(BaseModel):
    name:str
    phone:int
    email:str
    password:str

class Loginuser(BaseModel):
    email:str
    password:str