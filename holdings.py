#!/usr/bin/python

"""
Database accessors for grabbing current holdings
"""

DB_FILE="db/holdings.db"

import unittest
import sqlite3

class Holding(object):
    def __init__(self, symbol, holding, purchase_price, date):
        self.symbol=symbol
        self.holding=holding
        self.purchase_price = purchase_price
        self.purchase_date = date

    def save(self, cursor):
        sql = """insert into holdings (symbol, holding, purchase_price, purchase_date)
                values ('{0}', {1}, {2}, '{3}');""".format( self.symbol,
                                                           self.holding,
                                                           self.purchase_price,
                                                           self.purchase_date)
        cursor.execute(sql)
        
class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(DB_FILE)
        self.cursor = self.db.cursor()
        self.new_holding = Holding("AFI.AX", 1601, 6.16, "2015-01-02 14:30:00.000")
        self.new_holding.save(self.cursor)
        
    def testGetHoldings(self):
        cursor=self.cursor
        
    def tearDown(self):
        self.db.close()

if __name__=="__main__":
    unittest.main()
