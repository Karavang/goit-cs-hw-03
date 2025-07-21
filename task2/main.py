from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/db?retryWrites=true&w=majority")
db = client.book


def readAll():
    data = db.cats.find()
    return list(data)


def deleteOne(name: str):
    db.cats.delete_one({"name": name})
    return f"{name} don't with us"


def drop():
    db.cats.drop()
    return "db was dropped"


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


print(readAll())
