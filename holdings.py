#!/usr/bin/python

"""
Database accessors for grabbing current holdings
"""

import unittest
import sqlite3
import datetime
import YahooFinance
import configdb

DB_FILE="db/holdings.db"
timeFormat = fmt="%Y-%m-%d %H:%M:%S"

def getHoldings():
    db=sqlite3.connect(DB_FILE)
    cursor=db.cursor()
    holdings=Holdings()
    holdings.load(cursor)
    cursor.close()
    db.close()
    return holdings

#A list of Holding objects 
class Holdings(object):
    def __init__(self):
        self.holdings=[]
        self.lastReloadTime = configdb.getConfig('last_reload')

    #Load holdings from db and get prices from Yahoo!
    def load(self, cursor):
        if self.shouldReload():
            self.loadHoldings(cursor)
            self.getPrices()
        else:
            self.loadFromCache()
    
    #Load all holdings from database
    def loadHoldings(self, cursor):
        sql = "select symbol, holding, purchase_price, purchase_date from holdings;"
        cursor.execute(sql)
        for row in cursor:
            holding = Holding(row[0], row[1], row[2], row[3])
            self.holdings.append(holding)

    #Ask Yahoo! for the prices
    def getPrices(self):
        quotes = YahooFinance.YahooQuotes(self.allSymbols())
        for holding in self.holdings:
            holding.name = quotes[holding.symbol].name
            holding.offer = quotes[holding.symbol].offer
            holding.bid = quotes[holding.symbol].bid
        #Record as last reload
        now=datetime.datetime.now()
        self.lastReloadTime = now
        now_str=now.strftime(timeFormat)
        configdb.setConfig('last_reload', now_str)

    def loadFromCache(self):
        pass
            
    #Should we reload yet?
    def shouldReload(self):
        now = datetime.datetime.now()
        return (self.lastReload() + self.minReload()) < now

    #When did we last hit Yahoo!?
    def lastReload(self):
        str_time = configdb.getConfig('last_reload')
        #Parse the datetime
        return datetime.datetime.strptime(str_time, timeFormat)

    #how long should we wait for a reload?
    def minReload(self):
        str_delay = configdb.getConfig('min_reload')
        return datetime.timedelta(seconds=int(str_delay))

    def allSymbols(self):
        return [holding.symbol for holding in self.holdings]

    def totalValue(self):
        return sum([holding.value() for holding in self.holdings])

    def totalCost(self):
        return sum([holding.purchaseCost() for holding in self.holdings])

    def totalProfit(self):
        return sum([holding.profit() for holding in self.holdings])
    
    def __getitem__(self, key):
        return self.holdings[key]

    def __len__(self):
        return len(self.holdings)

    def __unicode__(self):
        s=""
        for holding in self.holdings:
            s += str(holding) + "\r\n"
        return s
        
    def __str__(self):
        return self.__unicode__()

    def toHTML(self):
        html='<table class="holdings">\r\n'
        html+='<thead>'
        html+='<tr><th>Symbol</th><th>Name</th><th>Holding</th><th>Bid</th><th>Value</th><th>Profit</th></tr>\r\n'
        html += '</thead>\r\n'
        html += '<tbody>\r\n'
        for holding in self.holdings:
            html += holding.toHTML() + '\r\n'
        html += '</tbody>\r\n'
        html+='</table>\r\n'
        html += '<h4>Total cost: ${0}</h4>\r\n'.format(self.totalCost())
        html += '<h4>Total value: ${0}</h4>\r\n'.format(self.totalValue())
        html += '<h4>Total profit: ${0}</h4>\r\n'.format(self.totalProfit())
        return html
    
#A single stock holding
class Holding(object):
    def __init__(self, symbol, holding, purchase_price, date):
        self.symbol=symbol
        self.holding=holding
        self.purchase_price = purchase_price
        self.purchase_date = date
        self.bid=None
        self.offer=None
        
    def save(self, cursor):
        sql = """insert into holdings (symbol, holding, purchase_price, purchase_date)
                values ('{0}', {1}, {2}, '{3}');""".format( self.symbol,
                                                           self.holding,
                                                           self.purchase_price,
                                                           self.purchase_date)
        cursor.execute(sql)

    def value(self):
        price=0.0
        try:
            price = float(self.bid)
        except (ValueError, TypeError):
            price=0.0
        return self.holding * price

    def purchaseCost(self):
        price=0.0
        try:
            price = float(self.purchase_price)
        except (ValueError, TypeError):
            price=0.0
        return self.holding * price

    def profit(self):
        return self.value() - self.purchaseCost()
    
    def __unicode__(self):
        return "symbol:{0} holding:{1} bid: {2} offer: {3} cost: ${4} value: ${5} profit:${6}".format(self.symbol, 
                                                                  self.holding,
                                                                  self.bid,
                                                                  self.offer,
                                                                  self.purchaseCost(),
                                                                  self.value(),
                                                                  self.profit())
    
    def __str__(self):
        return self.__unicode__()

    #Return a representation as an HTML table row
    def toHTML(self):
        html = '<tr class="holding">'
        html += '<td>{0}</td>'.format(self.symbol)
        html += '<td>{0}</td>'.format(self.name)
        html += '<td>{0}</td>'.format(self.holding)
        html += '<td>{0}</td>'.format(self.bid)
        html += '<td>{0}</td>'.format(self.value())
        html += '<td>{0}</td>'.format(self.profit())        
        html += '</tr>'
        return html


######## Unit tests
class TestHolding(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(DB_FILE)
        self.cursor = self.db.cursor()
        self.new_holding = Holding("AFI.AX", 1601, 6.16, "2015-01-02 14:30:00.000")
        self.new_holding.save(self.cursor)
        
    def testGetHoldings(self):
        cursor=self.cursor
      
    def tearDown(self):
        self.db.close()

class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(DB_FILE)
        self.cursor=self.db.cursor()

    def testLoadAll(self):
        holdings = Holdings()
        holdings.loadHoldings(self.cursor)
        self.assertEqual(len(holdings), 6)

    def testAll(self):
        h=getHoldings()
        print h.toHTML()
        
    def tearDown(self):
        self.db.close()
        
if __name__=="__main__":
    unittest.main()
