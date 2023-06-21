from dotenv import load_dotenv
import requests
import os

# Cargar las variables de entorno
load_dotenv()

# Consumir el endpoint de usuarios y obtener los datos
def consultar():
    url = os.getenv("API_USERS")
    response = requests.get(url)
    return response.json()