from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from app.core.config import SessionLocal, engine, get_db
from app.crud.auth_validacion import user_by_username
from app.models.usuario_model import Usuarios
from app.crud.usuario_crud import get_usuarios, crear_usuario, actualizar_usuario


from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')  
ALGORITHM = os.getenv('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def encode_token(data: dict):
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = data.get("username")
        user = user_by_username(db, username) 
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")