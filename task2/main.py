from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO"))
db = client.book
# db.cats.insert_one(
#     {
#         "name": "barsik",
#         "age": 3,
#         "features": ["ходить в капці", "дає себе гладити", "рудий"],
#     }
# )


def readAll():
    data = db.cats.find()
    return list(data)


def readByName(name):
    return db.cats.find_one({"name": name})


def deleteOne(name: str):
    db.cats.delete_one({"name": name})
    return f"{name} don't with us"


def drop():
    db.cats.delete_many({})
    return "All data has been deleted from the database"


def updateAge(name, age):
    data = db.cats.update_one({"name": name}, {"$set": {"age": age}})
    return db.cats.find_one({"name": name})


def addNewProp(name, newProp):
    data = db.cats.find_one({"name": name})
    print(data)
    features = data.get("features", [])
    if features:
        features.append(newProp)
    else:
        features = [newProp]
    db.cats.update_one({"name": name}, {"$set": {"features": features}})
    return f"{name}, тепер про тебе більше інформації"


print(readByName("barsik"))
