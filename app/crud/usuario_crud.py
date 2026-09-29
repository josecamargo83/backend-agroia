from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.usuario_model import Usuarios
from app.models.tipo_usuario_model import TipoUsuario
from app.models.estado_usuario_model import EstadoUsuario
from app.schemas.usuario_schemas import UsuarioCreate, UsuarioUpdate


def get_usuarios(db: Session):
    return db.query(Usuarios).all()


def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuarios).filter(
        Usuarios.Usuario_Id == usuario_id
    ).first()


def get_usuario_por_username(db: Session, username: str):
    return db.query(Usuarios).filter(
        Usuarios.Usuario_Nombre == username
    ).first()


def crear_usuario(db: Session, user: UsuarioCreate):
    existing_user = get_usuario_por_username(db, user.Usuario_Nombre)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )

    db_usuario = Usuarios(**user.dict())

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


def actualizar_usuario(db: Session, usuario_id: int, user: UsuarioUpdate):
    db_user = db.query(Usuarios).filter(
        Usuarios.Usuario_Id == usuario_id
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    existing_user = db.query(Usuarios).filter(
        Usuarios.Usuario_Nombre == user.Usuario_Nombre,
        Usuarios.Usuario_Id != usuario_id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado por otro usuario"
        )

    db_user.Usuario_Id = user.Usuario_Id
    db_user.Usuario_Nombres = user.Usuario_Nombres
    db_user.Usuario_Mail = user.Usuario_Mail
    db_user.Usuario_Telefono = user.Usuario_Telefono
    db_user.Usuario_Nombre = user.Usuario_Nombre
    db_user.Usuario_Password = user.Usuario_Password
    db_user.TipoUsuario_Id = user.TipoUsuario_Id
    db_user.EstadoUsuario_Id = user.EstadoUsuario_Id

    db.commit()
    db.refresh(db_user)

    return db_user


def get_tipos(db: Session):
    tipos = db.query(TipoUsuario).all()

    return [
        {
            "value": t.TipoUsuario_Id,
            "label": t.TipoUsuario_Descripcion
        }
        for t in tipos
    ]


def get_estados(db: Session):
    estados = db.query(EstadoUsuario).all()

    return [
        {
            "value": e.EstadoUsuario_Id,
            "label": e.EstadoUsuario_Descripcion
        }
        for e in estados
    ]