import certifi
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDB:
    def __init__(self, conn, dbname, collec):
        self.conn = conn
        self.dbname = dbname
        self.collec = collec

    def connect(self):
        try:
            client = MongoClient(self.conn, tlsCAFile=certifi.where())
            if client.admin.command('ping') == {'ok': 1.0}:
                print("Connection to MongoDB successful!")
            else:
                print("Connection to MongoDB failed.")            
            return client
        except ConnectionFailure as e:
            print(f"Connection to MongoDB failed: {e}")

    def load_data(self, data):
        try:
            collection = self.connect()[self.dbname][self.collec]
            _list = data['superside']['conversation']
            if len(_list) == 1:
                collection.insert_one(data)
            else:
                collection.insert_many(_list)
            print(f"{len(_list)} response(s) loaded on db {self.dbname} and collection {self.collec}!")
        except Exception as e:
            print(e)

    def delete_all_data(self):
        try:
            collection = self.connect()[self.dbname][self.collec]
            collection.delete_many({})
            print(f"All data deleted from db {self.dbname} and collection {self.collec}!")
        except Exception as e:
            print(e)