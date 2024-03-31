from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class DeviceBase(BaseModel):
    id_user: int
    name: str

class ColorBase(BaseModel):
    id_user: int
    hex_code: str

class DeviceColorBase(BaseModel):
    device_id: int
    color_id: int