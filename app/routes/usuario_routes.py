from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db
import app.crud.usuario_crud as crud
import app.schemas.usuario_schemas as schemas

app = APIRouter()

@app.get("/list")
def list_users(db: Session = Depends(get_db)):
    return crud.get_usuarios(db=db)

@app.get("/userId/{usuario_id}", response_model=schemas.UsuarioBase)
def id_user(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db=db, usuario_id=usuario_id)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

@app.post("/create", response_model=schemas.UsuarioCreate)
def user_create(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db=db, user=user)

@app.put("/update/{usuario_id}", response_model=schemas.UsuarioBase)
def user_update(usuario_id: int, user: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = crud.actualizar_usuario(db=db, usuario_id=usuario_id, user=user)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

@app.get("/types")
def list_user_types(db: Session = Depends(get_db)):
    return crud.get_tipos(db)

@app.get("/statuses")
def list_user_statuses(db: Session = Depends(get_db)):
    return crud.get_estados(db)