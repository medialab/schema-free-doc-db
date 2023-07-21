import csv
import json
from typing import Generator

import casanova  # pip install casanova
import pymongo  # pip install pymongo
from pymongo.collection import Collection
from pymongo.database import Database
from tqdm import tqdm

CONFIG = "config.json"


def yield_data(datafile) -> Generator[dict, None, None]:
    print("counting data file length...")
    total = casanova.reader.count(datafile)
    with open(datafile, "r") as f:
        reader = csv.DictReader(f)
        for row in tqdm(
            reader,
            total=total,
            desc="Processing documents...",
        ):
            yield row


def database_connection(database: str) -> Database:
    print("connection to datbase...")
    with open(CONFIG, "r") as f:
        config = json.load(f)
        connection_URI = config["mongo"]["connection string URI"]
    client = pymongo.MongoClient(connection_URI)
    return client[database]


def get_collection(
    collection_name: str, drop: bool = False, database: str | Database = "test"
) -> Collection:
    if isinstance(database, Database):
        db = database
    else:
        db = database_connection(database=database)
    if drop:
        db.drop_collection(collection_name)
    return db[collection_name]
