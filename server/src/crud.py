from sqlalchemy.orm import Session
from .models import *
from .schemas import *
from typing import Dict, List
from sqlalchemy import select, func
import hashlib

md5_hash = hashlib.new('md5')

def get_devices_colors(db: Session) -> Dict[int, List[str]]:
    devices_colors_dict = {"1": 'putple'}

    # query = (
    #     select(Device, Color)
    #     .join(DeviceColor, Device.id == DeviceColor.device_id)
    #     .join(Color, DeviceColor.color_id == Color.id)
    #     .order_by(Device.id, Color.id)
    # )
    # result = db.execute(query)

    # for device, color in result:
    #     if device.id not in devices_colors_dict:
    #         devices_colors_dict[device.id] = []
    #     devices_colors_dict[device.id].append(color.hex_code)

    return devices_colors_dict

def _password_hashing(password):
    md5_hash = hashlib.new('md5')
    md5_hash.update(password.encode())
    return md5_hash.hexdigest()

def create_user(db: Session, user: UserBase):
    user.password = _password_hashing(user.password)
    db_user = User(username=user.username, password=user.password)
    add_row(db, db_user)
    return True

def get_user_by_username_and_password(db: Session, user: UserBase):
    user.password = _password_hashing(user.password)
    user1 = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if user1 is not None:
        return user1.id
    else:
        return None
    
def get_user_by_username(db: Session, user: UserBase):
    user1 = db.query(User).filter(User.username == user.username).first()
    return bool(user1)
    
def get_user_by_id(db: Session, id_user):
    user = db.query(User).filter(User.id == id_user).first()
    return user.username
    
def get_devices(db: Session, current_user_id):
    devices = db.query(Device).filter(Device.id_user == current_user_id).all()
    return devices

def get_device_by_name(db: Session, device: DeviceBase):
    device1 = db.query(Device).filter(Device.name == device.name).first()
    return bool(device1)

def create_device(db: Session, device: DeviceBase):
    db_device = Device(id_user=device.id_user, name=device.name)
    add_row(db, db_device)
    return True

def get_colors(db: Session):
    colors = db.query(Color).all()
    return colors

def get_color_by_name(db: Session, color: ColorBase):
    color1 = db.query(Color).filter(Color.hex_code == color.hex_code).first()
    return bool(color1)

def create_color(db: Session, color: ColorBase):
    db_color = Color(hex_code=color.hex_code)
    add_row(db, db_color)
    return True

def add_row(db: Session, db_row):
    db.add(db_row)
    db.commit()
    db.refresh(db_row)
