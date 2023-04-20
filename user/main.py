from fastapi import FastAPI
from app import api as UsersAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI() 
app.include_router(UsersAPI.app,tags=["api"])

@app.get("/")
def home():
    return {"USER API"}

register_tortoise(
    app,
    db_url="postgres://postgres:root@127.0.0.1/crud-fastAPI",
    modules={'models':['app.models',]},
    generate_schemas=True,
    add_exception_handlers=True
)