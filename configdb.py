#!/usr/bin/python

#Utility functions for config data
import unittest
import stockdb
import sqlite3

def getConfig(key):
    cursor = stockdb.getCursor()
    sql="select value from config where name=?"
    cursor.execute(sql, (key,))
    try:
        return cursor.next()[0]
    except (StopIteration):
        return None

def updateConfig(key, val):
    sql = "update config set value = ? where name = ?"
    stockdb.execute(sql, (val, key))
    
def setConfig(key, val):
    if getConfig(key) == None:
        sql= "insert into config (name, value) values(?, ?)"
        stockdb.execute(sql, (key,val))
    else:
        updateConfig(key, val)

def deleteConfig(key):
    sql = "delete from config where name = ?"
    stockdb.execute(sql, (key,))

    
class TestConfig(unittest.TestCase):
    def setUp(self):
       setConfig('testkey', 'testval')
        
    def testRead(self):
        val = getConfig('testkey')
        self.assertEqual(val, 'testval')

    def testMissing(self):
        self.assertEqual(getConfig('xyzzy'), None)
        
    def testUpdate(self):
        updateConfig('testkey', 'newval')
        self.assertEqual(getConfig('testkey'), 'newval')

    def testSetNew(self):
        setConfig('newkey', 'setval')
        self.assertEqual(getConfig('newkey'), 'setval')

    def testSetExisting(self):
        setConfig('testkey', 'newnew')
        self.assertEqual(getConfig('testkey'), 'newnew')

    def testDelete(self):
        setConfig('foo', 'bar')
        self.assertEqual(getConfig('foo'), 'bar')
        deleteConfig('foo')
        self.assertEqual(getConfig('foo'), None)
        
    def tearDown(self):
        map(deleteConfig, ['testkey','newkey','foo'])
if __name__=="__main__":
    unittest.main()

