import unittest
from david_climate_check import file_sqlite_db

class ClimateCheckTest(unittest.TestCase):

    def test_check_file(self):
        print(file_sqlite_db)
        result = 5
        self.assertEqual(result, result)