from sqlalchemy.orm import Session
from .models import *
from .schemas import *
from typing import Dict, List
from sqlalchemy import select, func
import hashlib

def get_devices_colors(db: Session, current_user_id = -1):
    if current_user_id == -1:
        query = (
        select(Device, Color)
        .join(DeviceColor, Device.id == DeviceColor.device_id)
        .join(Color, DeviceColor.color_id == Color.id)
        .order_by(Device.id, Color.id)
        )
    else:
        query = (
            select(Device, Color)
            .join(DeviceColor, Device.id == DeviceColor.device_id)
            .join(Color, DeviceColor.color_id == Color.id)
            .where(Device.id_user == current_user_id)
            .order_by(Device.id, Color.id)
        )
    result = db.execute(query)

    return result

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

def get_colors(db: Session, current_user_id):
    colors = db.query(Color).filter(Color.id_user == current_user_id).all()
    return colors

def get_color_by_name(db: Session, color: ColorBase):
    color1 = db.query(Color).filter(Color.hex_code == color.hex_code).first()
    return bool(color1)

def create_color(db: Session, color: ColorBase):
    db_color = Color(id_user = color.id_user, hex_code=color.hex_code)
    add_row(db, db_color)
    return True

def add_row(db: Session, db_row):
    db.add(db_row)
    db.commit()
    db.refresh(db_row)

def deleting_repeat(db: Session, d_c: DeviceColorBase):
    db.query(DeviceColor).filter(DeviceColor.device_id ==d_c.device_id).delete()
    db.commit()

def add_device_color(db: Session, d_c: DeviceColorBase):
    deleting_repeat(db, d_c)
    device_color = DeviceColor(device_id=d_c.device_id, color_id=d_c.color_id)
    add_row(db, device_color)
