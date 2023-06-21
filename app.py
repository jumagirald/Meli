from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps
from dotenv import load_dotenv
import os
import consumo_datos_api

# Inicia el servidor con Flask
app = Flask(__name__)

# Cargar las variables de entorno del ambiente
load_dotenv()
usuario_bd = os.getenv("USER")
password_bd = os.getenv("PASSWORD")
api_key = os.getenv("API_KEY")

# Establecer la conexión a la base de datos de MongoDB
client = MongoClient(f"mongodb+srv://{usuario_bd}:{password_bd}@dbmercadolibre.v4yvzul.mongodb.net/")
db = client[os.getenv("DATABASE")]
collection = db[os.getenv("COLLECTION")]


# Validar api key que este AUTORIZADO
def validar_autorizacion(key:str):
    if(str(api_key) == key):
        return True
    else:
        return False

# Enpoint para insertar datos de usuarios consumidas de la API Externa
@app.route("/api/insertar", methods=['POST'])
def insertar_usuarios():

     # Consultar datos api externa
    data = consumo_datos_api.consultar()

    # Insertar los datos en la colección de MongoDB
    collection.insert_many(data)

    return '', 201

# Consultar datos de los usuarios con autorizacion de API-KEY
@app.route("/api/consultar", methods=['GET'])
def consultar_datos():
    if 'api-key' in request.headers:
        validacion = validar_autorizacion(request.headers['api-key'])
        if(validacion):
            datos =[]
            for dato in collection.find():
                datos.append(dato)

            return dumps(datos), 200

    return 'No autorizado', 401

# Verificar el estado del servicio
@app.route("/api/estado", methods=['GET'])
def estado_aplicacion():
    return "Corriendo!!", 200

# Correr servidor por el puerto 5000
if __name__=='__main__':
    app.run(host='127.0.0.1', port='5000')




