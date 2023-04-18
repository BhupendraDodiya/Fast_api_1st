from fastapi import APIRouter,Request,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from .models import user
from passlib.context import CryptContext
import typing
from fastapi_login import LoginManager

router = APIRouter()
SECRET = 'your-secret-key'
templates = Jinja2Templates(directory="app/templates")
manager=LoginManager(SECRET, token_url='/auth/token/')
pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# def flash(request: Request, message: typing.Any, category: str = "") -> None:
#     if "_messages" not in request.session:
#         request.session["_messages"] = []
#     request.session["_messages"].append({"message": message, "category": category})


# def get_flashed_messages(request: Request):
#     print(request.session)
#     return request.session.pop("_messages") if "_messages" in request.session else []

# templates.env.globals['get_flashed_messages'] = get_flashed_messages

@router.get("/",response_class=HTMLResponse)
async def read_item(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,})

@router.get("/login/",response_class=HTMLResponse)
async def read_item(request:Request):
    return templates.TemplateResponse("login.html",{"request":request,})

@router.get("/welcome/",response_class=HTMLResponse)
async def read_item(request:Request):
    return templates.TemplateResponse("welcome.html",{"request":request,})


@router.post("/registration/",response_class=HTMLResponse)
async def read_item(request:Request,
                    name: str = Form(...),
                    email: str = Form(...),
                    phone: str = Form(...),
                    password: str = Form(...)):
    if await user.filter(email=email).exists():
        # flash(request,'email already regster')
        return RedirectResponse('/',status_code=status.HTTP_302_FOUND)
    
    elif await user.filter(phone=phone).exists():
        # flash(request,'phone number already regster')
        return RedirectResponse('/',status_code=status.HTTP_302_FOUND)
    
    else:
        await user.create(name=name,email=email,phone=phone,password=get_password_hash(password))
        # flash(request,'User sucessfully register')
        return RedirectResponse('/login/',status_code=status.HTTP_302_FOUND)
    
@manager.user_loader()
async def load_user(phone: str):
    if await user.exists(phone=phone):
        persone = await user.get(phone=phone)
        return persone


@router.post('/loginuser/')
async def login(request: Request, Phone: str = Form(...),
                Password: str = Form(...)):
    Phone = Phone
    user = await load_user(Phone)
    if not user:
        return {'USER NOT REGISTERED'}
    elif not verify_password(Password, user.password):
        return {'PASSWORD IS WRONG'}
    access_token = manager.create_access_token(
        data=dict(sub=Phone)
    )
    if "_messages" not in request.session:
        request.session['_messages'] = []
        new_dict = {"user_id": str(
            user.id), "Phone": Phone, "access_token": str(access_token)}
        request.session['_messages'].append(
            new_dict
        )
    return RedirectResponse('/welcome/', status_code=status.HTTP_302_FOUND)