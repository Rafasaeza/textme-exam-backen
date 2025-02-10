from pymongo import MongoClient

def get_database(dbName: str):
    # URL de conexión, asegúrate de reemplazar <username>, <password>, <cluster-url> y <database-name> con los valores adecuados.
    CONNECTION_STRING = "mongodb+srv://examUser:mongoUma@cluster0.xszfu.mongodb.net/?"

    # Crear una conexión usando MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Especificar la base de datos que se desea usar
    return client[dbName]