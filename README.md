# Schema-free Document Database

Schema-free document database using open-source [FerretDB](https://github.com/FerretDB/FerretDB), "an open-source proxy, converting the MongoDB 6.0+ wire protocol queries to SQL - using PostgreSQL or SQLite as a database engine."

FerretDB is pitched as the "de-facto open-source substitute to MongoDB." Unfortunately, FerretDB does not (yet) support nested JSON arrays, which are one of the best parts of a MongoDB document database. However, another great aspect of MongoDB databases is the ease of dumping documents with different schemas into a collection. Plus, FerretDB's service supports requests sent in a Python script using the `pymongo` library.

Here's an example of how data from a CSV file can be parsed, manipulated, and inserted into the document database.

Input
|id|user_name|post|post_time|
|--|--|--|--|
|1|FionaA|"Hello world!"|2023-07-21 08:14:44.826259|

Output

```json
{
  "_id": {
    "$oid": "64ba4cc917022a377d337a25"
  },
  "id": "1",
  "user_name": "FionaA",
  "post": "Hello world!",
  "post_time": "2023-07-21 08:14:44.826259",
  "words": ["Hello", "world!"]
}
```

Contents

- [Set up](#set-up)
- [Usage](#usage)
- [Graphic User Interface (GUI)](#graphic-user-interface)

## Set up

### Set up database

Use Docker to install [FerretDB](https://github.com/ferretdb/FerretDB/pkgs/container/ferretdb).

```shell
$ docker pull ghcr.io/ferretdb/ferretdb:1.6.0
```

Start the FerretDB service the background.

```shell
$ docker compose up -d.
```

To verify that the service is running as a daemon with the following command, replace `<DATABASE>` with the name of a database on the FerretDB cluster. This command will open a shell based on `mongosh`, in which you can interact with the target database.

```shell
$ docker run --rm -it --network=ferretdb --entrypoint=mongosh mongo   "mongodb://username:password@ferretdb/<DATABASENAME>?authMechanism=PLAIN"
```

To explore the FerretDB shell's commands, enter:

```shell
DATABASENAME> db.help()
```

To exit the shell, enter: `Ctrl+C` twice.

To stop the FerretDB service, enter:

```shell
$ docker compose down
```

### Set up Python package

Create a virtual environment in Python 3.11.

Install dependencies.

```shell
$ pip install --r requirements.txt
```

## Usage

Import a CSV file into the document database.

```shell
$ python src/main.py --database-name <DATABASE> --collection-name <COLLECTION> import example.data.csv
```

Between parsing a CSV row into a dictionary and inserting it into the document database, you can manipulate the data, adding fields and enrichments. There are no limitations on how many new key-value pairs can be added to a row because MongoDB is flexible and does not require a rigid schema. However, due to FerretDB's limitations, no key's value can be a nested JSON array.

```python
    # Stream the CSV file
    for data in yield_data(datafile=datafile):
        # ---------- #
        # Do things to the CSV dict row...
        data.update({"words": data["post"].split()})
        # ---------- #

        # Dump the data in the collection
        collection.insert_one(document=data)
```

Export the collection to a JSON file.

```shell
$ python src/main.py --database-name <DATABASE> --collection-name <COLLECTION> export
```

## Graphic User Interface

The best open-source option for visually exploring the FerretDB / MongoDB database contents is an extension in VSCode for [MongDB](https://github.com/mongodb-js/vscode), which has an Apache 2.0 license. To connect your database to VSCode, the database service must first be running.

1. Open VSCode.
2. Install the `MongDB for VSCode` extension.
3. At the top of the screen, click `View` > `Command Palette` > `MongoDB Connect with String Connection`.
4. Input the connection string URI: "`mongodb://username:password@127.0.0.1/ferretdb?authMechanism=PLAIN`"
5. Make sure the Activity Bar is visible in VSCode. (`View` > `Appearance` > `Activity Bar`)
6. On the Activity Bar, scroll and find the MongoDB icon (an upright leaf), click it, and navigate your FerretDB / MongoDB connections and their databases.
