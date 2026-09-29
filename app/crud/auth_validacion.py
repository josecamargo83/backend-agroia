from sqlalchemy.orm import Session

from app.models.usuario_model import Usuarios

from app.schemas.usuario_schemas import UsuarioUpdate


def login_user(db: Session, username: str, password: str):
    usuario = db.query(Usuarios).filter(
        Usuarios.Usuario_Nombre == username,
        Usuarios.Usuario_Password == password
    ).first()

    return usuario


def user_by_username(db: Session, username: str):
    return db.query(Usuarios).filter(
        Usuarios.Usuario_Nombre == username
    ).first()


def user_by_email(db: Session, email: str):
    return db.query(Usuarios).filter(
        Usuarios.Usuario_Mail == email
    ).first()