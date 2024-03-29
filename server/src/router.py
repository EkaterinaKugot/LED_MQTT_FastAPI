from database import SessionLocal, engine, Base
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .crud import *
from .schemas import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

