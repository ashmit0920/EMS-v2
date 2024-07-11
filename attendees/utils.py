from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
CONN_STR = os.getenv("CONN_STR")

def get_db():
    client = MongoClient(CONN_STR)
    db = client['attendees']
    return db
