from server import SessionLocal, engine, Base
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .crud import *
from .schemas import *
from . import models

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

current_user_id = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def login_form():
    return HTMLResponse("""
    <html>
        <head>
            <title>Login</title>
        </head>
        <body>
            <h2>Вход</h2>
            <form action="/processing_login" method="post">
                <label for="username">Логин</label><br>
                <input type="text" id="username" name="username" placeholder="Логин" required style="margin-bottom:10px;"><br>
                <label for="password" >Пароль</label><br>
                <input type="password" id="password" name="password" placeholder="Пароль" required><br><br>
                <input type="submit" value="Войти">
            </form>
            <a href="/registration">Регистрация</a>
        </body>
    </html>
    """)

@router.post("/processing_login")
def processing_login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    global current_user_id
    user = UserBase(username=username, password=password)
    current_user_id = get_user_by_username_and_password(db, user)
    if current_user_id is not None:
        return RedirectResponse("/devices_colors")
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
@router.get("/registration")
def registration_form():
    return HTMLResponse("""
    <html>
        <head>
            <title>Registration</title>
        </head>
        <body>
            <h2>Регистрация</h2>
            <form action="/processing_registration" method="get">
                <label for="username">Логин</label><br>
                <input type="text" id="username" name="username" placeholder="Логин" required style="margin-bottom:10px;"><br>
                <label for="password" >Пароль</label><br>
                <input type="password" id="password" name="password" placeholder="Пароль" required><br><br>
                <input type="submit" value="Зарегистрироваться">
            </form>
            <a href="/registration">Регистрация</a>
        </body>
    </html>
    """)

@router.get("/processing_registration")
def processing_registration(username: str, password: str, db: Session = Depends(get_db)):
    user = UserBase(username=username, password=password)
    if get_user_by_username(db, user):
        create_user(db, user)
    else:
        raise HTTPException(status_code=401, detail="There is a user with this name")
    return RedirectResponse("/")
    
@router.post("/devices_colors")
def login_form():
    return f"{current_user_id}"


@router.get("/admin")
def pub_devices_colors(db: Session = Depends(get_db)):
    return get_devices_colors(db)