from dagster import resource
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBResource:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client[os.getenv('MONGO_DB')]

    def get_collection(self, collection_name):
        return self.db[collection_name]

@resource
def mongo_resource():
    return MongoDBResource() 