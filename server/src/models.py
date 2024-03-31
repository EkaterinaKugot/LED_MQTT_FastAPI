from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    devices = relationship("Device", back_populates="user")
    colors = relationship("Color", back_populates="user")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    name = Column(String)

    user = relationship("User", back_populates="devices")
    device_colors = relationship("DeviceColor", back_populates="device")

class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    hex_code = Column(String)

    user = relationship("User", back_populates="colors")
    device_colors = relationship("DeviceColor", back_populates="color")


class DeviceColor(Base):
    __tablename__ = "devices_colors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    color_id = Column(Integer, ForeignKey('colors.id'))

    device = relationship("Device", back_populates="device_colors")
    color = relationship("Color", back_populates="device_colors")