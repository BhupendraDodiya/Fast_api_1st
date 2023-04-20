from .pydantic_models import Person,Loginuser,Token,Delete,Update,One
from .models import *
from passlib.context import CryptContext
from fastapi import APIRouter
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder


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
        return {"status":False, 'message':'phone number already exist'}
    elif await user.exists(email=data.email):
        return {"status":False, 'message':'email already exist'}
    else:
        user_obj = await user.create(email=data.email,name=data.name,phone=data.phone,
                                     password=get_password_hash(data.password))
        return user_obj
    
@manager.user_loader()
async def load_user(phone: str):
    if await user.exists(phone=phone):
        persone = await user.get(phone=phone)
        return persone
    
@app.post('/login/')
async def login(data: Loginuser):
    phone = data.phone
    user = await load_user(phone)

    if not user:
        return JSONResponse({'status':False,'message':'User not registered'},status_code=403)
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False,'message':'Invalid password'},status_code=403)
    access_token = manager.create_access_token(
        data = {'sub':dict({'id':jsonable_encoder(user.id)}),}
    )

    new_dict = jsonable_encoder(user)
    new_dict.update({'access_token':access_token})
    return Token(access_token=access_token,Token_type='bearer')

@app.get('/data/')
async def all_user():
    User = await user.all()
    return User

@app.post('/data_one/{id}')
async def one_user(data:One):
    User = await user.get(id=data.id)
    return User

@app.delete('/delete_all/')
async def all_user():
    await user.all().delete()
    return {'status':True,'message':'all user delete'}

@app.delete("/delete_user/{id}")
async def delete(data:Delete):
    await user.filter(id=data.id).delete()
    return {'status':True,'message':'user delete'}

@app.put("/update_user/{id}")
async def update(data:Update):
    if await user.exists(phone=data.phone):
        return {"status":False, 'message':'phone number already exist'}
    elif await user.exists(email=data.email):
        return {"status":False, 'message':'email already exist'}
    else:
        user_obj = await user.filter(id=data.id).update(email=data.email,name=data.name,phone=data.phone,
                                     password=get_password_hash(data.password))
        return  {"status":True, 'message':'user update successfully'}