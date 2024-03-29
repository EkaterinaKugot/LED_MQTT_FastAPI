from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class DeviceBase(BaseModel):
    name: str

class ColorBase(BaseModel):
    hex_code: str

class DeviceColorBase(BaseModel):
    device_id: int
    color_id: int