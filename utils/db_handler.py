from os import getenv
from typing import Final
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

from Models.User import User

class DB_Handler:
    def __init__(self) -> None:
        load_dotenv(".env")
        uri : Final = getenv("MONGO_DB_CONNECTION_STRING")

        # Create a new client and connect to the server
        client = MongoClient(uri)
        print(client)

        # Send a ping to confirm a successful connection
        try:
            # list out the list of the databases
            print(client.list_database_names())
        except Exception as e:
            print(f'Failed to connect db :: ${e}')

