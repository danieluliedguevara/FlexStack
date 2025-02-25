import unittest
from unittest.mock import MagicMock

from flexstack.facilities.local_dynamic_map.database import DataBase


class TestDatabase(unittest.TestCase):
    def test__init__(self):
        DataBase(database_name="test_database")

    def test_delete(self):
        database = DataBase(database_name="test_database")
        database.delete(database_name="test_database")

    def test_search(self):
        database = DataBase(database_name="test_database")
        database.search(MagicMock())

    def test_insert(self):
        database = DataBase(database_name="test_database")
        database.insert(data=None)

    def test_get(self):
        database = DataBase(database_name="test_database")
        database.get(index=None)

    def test_update(self):
        database = DataBase(database_name="test_database")
        database.update(data=None, index=None)

    def test_remove(self):
        database = DataBase(database_name="test_database")
        database.remove(data_object=None)

    def test_all(self):
        database = DataBase(database_name="test_database")
        database.all()

    def test_exists(self):
        database = DataBase(database_name="test_database")
        database.exists(field_name="test_field_name")


if __name__ == "__main__":
    unittest.main()
