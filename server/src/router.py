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
            <h3>Вход</h3>
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
            <h3>Регистрация</h3>
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
    if not get_user_by_username(db, user):
        create_user(db, user)
    else:
        raise HTTPException(status_code=401, detail="There is a user with this name")
    return RedirectResponse("/")
    
@router.post("/devices_colors")
def login_form(db: Session = Depends(get_db)):
    devices = get_devices(db, current_user_id)
    colors = get_colors(db)
    option_device = ""
    for device in devices:
        option_device += f"<option value='{device.id}'>{device.name}</option>"

    option_color = ""
    for color in colors:
        option_color += f"<option value='{color.id}'>{color.hex_code}</option>"

    username = get_user_by_id(db, current_user_id)

    return HTMLResponse(f"""
    <html>
        <head>
            <title>Matching device and color</title>
        </head>
        <body>
            <h2>Профиль: {username}</h2>
            <a href="/add_device" style="margin-right: 20px">Добавить устройство</a>
            <a href="/add_color" style="margin-right: 50px">Добавить комбинацию цветов</a>
            <a href="/">Выход</a>
            <h3>Соотнесение устройства и цветов</h3>
            <form action="/processing_matching" method="post">
                <label for="devices">Устройства</label><br>
                <select id="devices" name="devices">
                    <option value="device1">Устройство 1</option>
                    {option_device}
                </select><br><br>
                <label for="colors">Комбинации цветов</label><br>
                <select id="colors" name="colors">
                    <option value="red">Красный</option>
                    {option_color}
                </select><br><br>
                <input type="submit" value="Соотнести">
            </form>
        </body>
    </html>
    """)

@router.get("/add_device")
def add_device(db: Session = Depends(get_db)):
    username = get_user_by_id(db, current_user_id)
    return HTMLResponse(f"""
    <html>
        <head>
            <title>Add device</title>
        </head>
        <body>
            <h2>Профиль: {username}</h2>
            <h3>Добавить устройство</h3>
            <form action="/аdding_device" method="post">
                <label for="name">Название</label><br>
                <input type="text" id="name" name="name" required"><br><br>
                <input type="submit" value="Добавить">
            </form>
        </body>
    </html>
    """)

@router.post("/аdding_device")
def аdding_device(name: str = Form(...), db: Session = Depends(get_db)):
    device = DeviceBase(id_user=current_user_id, name=name)
    if not get_device_by_name(db, device):
        create_device(db, device)
    else:
        raise HTTPException(status_code=401, detail="Such a device already exists")
    return RedirectResponse("/devices_colors")


@router.get("/admin")
def pub_devices_colors(db: Session = Depends(get_db)):
    return get_devices_colors(db)