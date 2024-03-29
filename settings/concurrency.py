import requests
from datetime import datetime, timedelta
from functools import lru_cache


BASE_URL = "https://mindicador.cl/api/"


def get_previous_weekday(date):
    """
    If the date falls on a weekend, return the previous Friday's date.
    Otherwise, return the date itself.
    """
    weekday = date.weekday()
    if weekday == 5:  # Saturday
        return date - timedelta(days=1)
    elif weekday == 6:  # Sunday
        return date - timedelta(days=2)
    return date


@lru_cache
def get_today_dolar() -> float:

    # Get the today's dolar value in Chile, in format DD-MM-YYYY, using datetime
    today = datetime.now()
    adjusted_date = get_previous_weekday(today)
    formatted_date = adjusted_date.strftime("%d-%m-%Y")

    # Get the dolar value from the API
    response = requests.get(f"{BASE_URL}dolar/{formatted_date}")
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
