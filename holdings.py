#!/usr/bin/python

"""
Database accessors for grabbing current holdings
"""

DB_FILE="db/holdings.db"

import unittest
import sqlite3

class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(DB_FILE)
        
    def testGetHoldings(self):
        cursor=self.db.cursor()
        
    def tearDown(self):
        self.db.close()xs

if __name__=="__main__":
    unittest.main()
