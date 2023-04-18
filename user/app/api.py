from .pydantic_models import Person
from .models import *
from passlib.context import CryptContext
from fastapi import APIRouter
from fastapi_login import LoginManager


app = APIRouter()
SECRET = 'your-secret-key'

manager=LoginManager(SECRET, token_url='/auth/token/')

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post('/ragistration_api/')
async def ragistration(data:Person):
    if await user.exists(phone=data.phone):
        return {"status":False, 'message':'phone number already exists'}
    elif await user.exists(email=data.email):
        return {"status":False, 'message':'phone number already exists'}
    else:
        user_obj = await user.create(email=data.email,name=data.name,phone=data.phone,
                                     password=get_password_hash(data.password))
        return user_obj
    
@manager.user_loader()
async def load_user(phone: str):
    if await user.exists(phone=phone):
        persone = await user.get(phone=phone)
        return persone