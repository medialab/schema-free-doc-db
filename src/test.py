import unittest

from utils import database_connection


class TestConnection(unittest.TestCase):
    collection_name = "collection1"

    def setUp(self):
        # Set up the database connection
        self.database = database_connection(database="chatgpt")
        self.database.drop_collection(self.collection_name)
        self.collection = self.database[self.collection_name]

    def test_connection(self):
        self.collection.insert_one({"name": "Fiona", "message": "hello world"})
        doc = self.collection.find_one({"name": "Fiona"})
        self.assertEquals(len([doc]), 1)

    def tearDown(self):
        self.database.drop_collection(self.collection_name)


if __name__ == "__main__":
    unittest.main()
