import os

from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def verificar_id_token_google(token: str):

    try:

        informacion = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        if informacion.get("iss") not in [
            "accounts.google.com",
            "https://accounts.google.com"
        ]:
            raise ValueError("Emisor del token inválido")

        if not informacion.get("email_verified"):
            raise ValueError(
                "El correo de Google no está verificado"
            )

        return informacion

    except Exception as e:

        raise ValueError(
            f"Token de Google inválido: {str(e)}"
        )