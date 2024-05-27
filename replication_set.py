import os
from idlelib.iomenu import errors

import json
import pymongo
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure


def charge_collection():
    """
    This method reads a JSON file containing database collection.

    :return: A dictionary containing the collection.
    """
    # with open("resources/db_config.yml", "r") as f:
    with open("resources/db_collections.json", "r") as f:
        return json.load(f)


def get_db_data():
    """
    Retrieves the database details from the environment variables.

    :return: A tuple containing the database db_name, user, and password.
    :rtype: tuple
    :raises EnvironmentError: If the required database credentials are not set in the environment.
    """
    # Carga las variables de entorno del archivo .env
    load_dotenv()
    # Obtener detalles de la base de datos
    db_name = os.getenv('DB_NAME2')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    if not all([db_name]):
        raise EnvironmentError('Database credentials (DB_NAME) not set in environment.')

    return db_name, user, password


def connect_mongo(db_name, user, password):
    """
    Connect to MongoDB.

    :param db_name: The db_name of the MongoDB database to connect to.
    :param user: The username used to authenticate with the database.
    :param password: The password used to authenticate with the database.
    :return: The database client connected to the specified database.

    Example:

        >>> client = connect_mongo('mydb', 'myuser', 'mypassword')
        >>> db = client['mydb']

    """
    try:
        client = pymongo.MongoClient('mongodb://{}:{}@CO-L300517:20000,CO-L300517:20001,CO-L300517:20002/{}'
                                     .format(user, password, db_name),
                                     replicaset='MRSTest')
        valid_connection(client)
        return client[db_name]
    except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure):
        print("Connection failed" + errors)


def valid_connection(client):
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ping')
        print('Connected successfully!')
    except ConnectionFailure:
        print('Server not available')


def create_collections():
    """
    Create collections in the database.

    :return: None
    """
    try:
        for collection in config["collections"]:
            collection_name = collection["name"]
            db_collection = db[collection_name]
            for field in collection["fields"]:
                key, _ = next(iter(field.items()))  # Get first (and only) key from the dictionary
                db_collection.create_index(key)
        print("Collections created successfully")
    except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure):
        print("create_collections failed" + errors)


def insert_data():
    """
    Insert data from JSON files into database collections.

    :return: None
    """
    try:
        for collection in config["collections"]:
            collection_name = collection["name"]

            path_file = f"resources/{collection_name}.json"

            # Check if the file exists. If not, print an error message and continue to the next collection
            if not os.path.isfile(path_file):
                print(f"Cannot find the JSON file: {path_file}")
                continue

            with open(path_file, "r", encoding='utf-8') as f:
                all_data = json.load(f)
            collection_in = db[collection_name]
            for data in all_data:
                collection_in.insert_one(data)
        print("Inserted data into collections")

    except (errors.ServerSelectionTimeoutError, errors.ConnectionFailure):
        print("insert_data failed" + errors)


if __name__ == '__main__':
    config = charge_collection()
    db_name, db_user, db_password = get_db_data()
    db = connect_mongo(db_name, db_user, db_password)
    create_collections()
    insert_data()
