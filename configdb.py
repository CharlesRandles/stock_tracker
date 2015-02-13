#!/usr/bin/python

#Utility functions for config data
import unittest
import stockdb

def getConfig(key):
    sql="select value from config where name='{0}'".format(key)
    stockdb.getCursor().execute(sql)
    try:
        val = stockdb.getCursor().next()[0]
    except (StopIteration):
        return None
    return val

def updateConfig(key, val):
    sql = "update config set value = '{1}' where name = '{0}'".format(key, val)
    stockdb.getCursor().execute(sql)

def setConfig(key, val):
    if getConfig(key) == None:
        sql= "insert into config (name, value) values('{0}', '{1}')".format(key, val)
        stockdb.getCursor().execute(sql)
    else:
        updateConfig(key, val)

def deleteConfig(key):
    sql = "delete from config where name = '{0}'".format(key)
    stockdb.getCursor().execute(sql)
        
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

