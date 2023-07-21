import ast
import json

import click
from bson.json_util import dumps

from utils import database_connection, get_collection, yield_data


@click.group()
@click.option("--database-name", required=True, help="name of the database")
@click.option("--collection-name", required=True, help="collection name in database")
@click.pass_context
def cli(ctx, database_name, collection_name):
    # Ensure that the context object exists and is a dictionary
    ctx.ensure_object(dict)

    # Store a connection to the database
    ctx.obj["database"] = database_connection(database=database_name)

    # Store the name of the target collection
    ctx.obj["collection"] = collection_name


@cli.command("import")
@click.argument("datafile")
@click.pass_context
def import_data(ctx, datafile):
    # Get the connection to the database collection
    collection = get_collection(
        database=ctx.obj["database"],  # Name of the target database
        collection_name=ctx.obj["collection"],  # Name of the collection
        drop=True,  # Whether to drop all documents in the collection to start over
    )

    # Stream the CSV file
    for data in yield_data(datafile=datafile):
        # ---------- #
        # Do things to the CSV dict row...
        data.update({"words": data["post"].split()})
        # ---------- #

        # Dump the data in the collection
        collection.insert_one(document=data)

    # Print a count of how many documents are in the collection
    doc_count = len([_ for _ in collection.find()])
    print(f"{doc_count} documents in the collection.")


@cli.command("export")
@click.pass_context
def export_data(ctx):
    # Get the connection to the database collection
    collection = get_collection(
        database=ctx.obj["database"],  # Name of the target database
        collection_name=ctx.obj["collection"],  # Name of the collection
        drop=False,  # Whether to drop all documents in the collection to start over
    )

    # Find all the documents matching the filter
    # Example given does not have any filter / returns everything
    cursor = collection.find()

    # Using pymongo's JSON utils dumps, dump collection to outfile
    with open("outfile.json", "w") as of:
        json.dump(json.loads(dumps(cursor)), of, indent=4)


if __name__ == "__main__":
    cli(obj={})
