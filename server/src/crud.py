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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def get_user_by_username_and_password(db: Session, user: UserBase):
    user.password = _password_hashing(user.password)
    user = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if user is not None:
        return user.id
    else:
        return None
    
def get_user_by_username(db: Session, user: UserBase):
    user = db.query(User).filter(User.username == user.username).first()
    if user is not None:
        return False
    else:
        return True
