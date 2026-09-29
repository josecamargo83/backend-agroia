import requests

from app.core.config import (
    INFLUXDB_URL,
    INFLUXDB_DATABASE,
    INFLUXDB_TOKEN
)


def consultar_influxdb(query: str):

    url = f"{INFLUXDB_URL}/api/v3/query_sql"

    headers = {
        "Authorization": f"Bearer {INFLUXDB_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "db": INFLUXDB_DATABASE,
        "q": query,
        "format": "json"
    }

    respuesta = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=10
    )

    respuesta.raise_for_status()

    return respuesta.json()