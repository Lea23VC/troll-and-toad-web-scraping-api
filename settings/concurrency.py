import requests
from datetime import datetime
from functools import lru_cache


BASE_URL = "https://mindicador.cl/api/"


@lru_cache
def get_today_dolar() -> float:

    # Get the today's dolar value in Chile, in format DD-MM-YYYY, using datetime
    today = datetime.now().strftime("%d-%m-%Y")

    # Get the dolar value from the API
    response = requests.get(f"{BASE_URL}dolar/{today}")
    data = response.json()

    # Example API response:
    """
    {
        "version": "1.7.0",
        "autor": "mindicador.cl",
        "codigo": "dolar",
        "nombre": "Dólar observado",
        "unidad_medida": "Pesos",
        "serie": [
            {
            "fecha": "2024-03-20T03:00:00.000Z",
            "valor": 962.06
            }
        ]
    }
    """

    # Get the dolar value from the API response
    dolar_value = data['serie'][0]['valor']

    return dolar_value
