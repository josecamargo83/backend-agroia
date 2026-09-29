from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.auth_token import encode_token
from app.core.config import get_db

import app.crud.auth_validacion as crud
import app.schemas.auth_schemas as schemas

from app.core.google_auth import verificar_id_token_google

import requests
import os
import secrets

from dotenv import load_dotenv

load_dotenv()

app = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "http://localhost:8000/auth/google/callback"
)


@app.post("/login")
def login(
    user_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    user = crud.login_user(
        db,
        user_data.username,
        user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = encode_token({
        "username": user.Usuario_Nombre
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "Usuario_Id": user.Usuario_Id,
            "Usuario_Nombres": user.Usuario_Nombres,
            "TipoUsuario_Id": user.TipoUsuario_Id
        }
    }


# ============================================================
# GOOGLE LOGIN
# ============================================================

@app.get("/google")
def login_google():

    google_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=select_account"
    )

    return RedirectResponse(
        url=google_url
    )


@app.get("/google/callback")
def google_callback(
    code: str,
    db: Session = Depends(get_db)
):

    try:

        # ====================================================
        # 1. INTERCAMBIAR CODE POR TOKENS
        # ====================================================

        respuesta = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI
            },
            timeout=10
        )

        if not respuesta.ok:

            raise HTTPException(
                status_code=401,
                detail="No fue posible obtener el token de Google"
            )

        tokens = respuesta.json()

        google_id_token = tokens.get("id_token")

        if not google_id_token:

            raise HTTPException(
                status_code=401,
                detail="Google no devolvió un ID Token"
            )

        # ====================================================
        # 2. VALIDAR ID TOKEN
        # ====================================================

        informacion = verificar_id_token_google(
            google_id_token
        )

        correo = informacion.get("email")
        nombre = informacion.get("name")

        if not correo:

            raise HTTPException(
                status_code=401,
                detail="Google no devolvió el correo"
            )

        if not nombre:

            nombre = correo.split("@")[0]

        # ====================================================
        # 3. BUSCAR USUARIO
        # ====================================================

        user = crud.user_by_email(
            db,
            correo
        )

        # ====================================================
        # 4. CREAR USUARIO SI NO EXISTE
        # ====================================================

        if not user:

            username_base = correo.split("@")[0]

            username = username_base[:50]

            # Evitar conflicto con Usuario_Nombre UNIQUE
            username_original = username
            contador = 1

            while crud.user_by_username(
                db,
                username
            ):

                sufijo = str(contador)

                username = (
                    username_original[:50 - len(sufijo)]
                    + sufijo
                )

                contador += 1

            # Contraseña aleatoria porque
            # este usuario utilizará Google
            password_google = secrets.token_urlsafe(32)

            from app.models.usuario_model import Usuarios

            user = Usuarios(
                Usuario_Nombres=nombre[:100],
                Usuario_Mail=correo[:150],
                Usuario_Telefono=None,
                Usuario_Nombre=username,
                Usuario_Password=password_google,
                TipoUsuario_Id=1,
                EstadoUsuario_Id=1
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        # ====================================================
        # 5. GENERAR JWT AGROIA
        # ====================================================

        token = encode_token({
            "username": user.Usuario_Nombre
        })

        # ====================================================
        # 6. REDIRIGIR AL FRONTEND
        # ====================================================

       
        return RedirectResponse(
            url=f"http://localhost:5500/index.html?token={token}"
        )

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error en autenticación con Google: {str(e)}"
        )