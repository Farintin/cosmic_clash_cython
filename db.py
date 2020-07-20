import json

with open("db.json", "r") as db:
    document = json.load(db)


def save(doc):
    with open("db.json", "w") as db:
        json.dump(doc, db, indent=4)
