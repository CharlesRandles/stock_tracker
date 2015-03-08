#!/usr/bin/python

"""
Database accessors for grabbing current holdings
"""

import unittest
import datetime
import YahooFinance
import configdb
import stockdb

DB_FILE="db/holdings.db"
timeFormat = fmt="%Y-%m-%d %H:%M:%S"

def getHoldings():
    cursor=stockdb.getCursor()
    holdings=Holdings()
    holdings.load()
    return holdings

#Helper for messing with timezones
def parseOffset(offset):
    hours = int(offset[0:3])
    minutes = int(offset[3:])
    return datetime.timedelta(hours=hours, minutes=minutes)

def toUTC(time, offset):
    return time - parseOffset(offset)

def nowUTC():
    offset = configdb.getConfig('server_utcoffset')
    now_utc=toUTC(datetime.datetime.now(), offset)
    return now_utc.strftime(timeFormat)

#A list of Holding objects 
class Holdings(object):
    def __init__(self):
        self.holdings=[]
        self.lastReloadTime = configdb.getConfig('last_reload')

    #Load holdings from db and get prices from Yahoo!
    def load(self):
        self.holdings=[]
        if self.shouldReload():
            self.loadHoldings()
            self.getPrices()
            self.source = "Yahoo!"
        else:
            self.loadFromCache()
            self.source="Cache"
    
    #Load all holdings from database
    def loadHoldings(self):
        cursor = stockdb.getCursor()
        sql = "select symbol, '', holding, purchase_price, purchase_date from holdings;"
        cursor.execute(sql)
        for row in cursor:
            holding = Holding(row[0], row[1], row[2], row[3], row[4])
            self.holdings.append(holding)

    #Ask Yahoo! for the prices
    def getPrices(self):
        quotes = YahooFinance.YahooQuotes(self.allSymbols())
        for holding in self.holdings:
            try:
                holding.name = quotes[holding.symbol].name
                holding.offer = quotes[holding.symbol].offer
                holding.bid = quotes[holding.symbol].bid
                holding.change = quotes[holding.symbol].change
            except (KeyError):
                holding.name = "Not found"
                holding.offer = 0.0
                holding.bid = 0.0
                holding.change = 0.0
        #Record as last reload
        now=datetime.datetime.now()
        self.lastReloadTime = now
        now_str=now.strftime(timeFormat)
        configdb.setConfig('last_reload', now_str)
        self.writeToCache()

    #Pull holdings and prices from cache table
    def loadFromCache(self):
        cursor = stockdb.getCursor()
        sql = """select symbol,
                        name,
                        holding,
                        purchase_price,
                        purchase_date,
                        bid,
                        offer,
                        change
                        from cache"""
        cursor.execute(sql)
        for row in cursor:
            holding = Holding(row[0],
                              row[1],
                              row[2],
                              row[3],
                              row[4],
                              row[5],
                              row[6],
                              row[7])
            self.holdings.append(holding)

    #Clear and re-populate cache table
    def writeToCache(self):
        stockdb.executeDirect('delete from cache')
        for holding in self.holdings:
            holding.cache()
    
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
    
    def dayProfit(self):
        return sum([holding.dayProfit() for holding in self.holdings])
    
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
        html+="""
        <tr>
            <th>Symbol</th>
            <th>Name</th>
            <th>Holding</th>
            <th>Purchase</th>
            <th>Bid</th>
            <th>Offer</th>
            <th>Value</th>
            <th>Profit</th>
            <th>Change</th>
            <th>Gain/Loss</th>
            </tr>\r\n"""
        html += '</thead>\r\n'
        html += '<tbody>\r\n'
        for holding in self.holdings:
            html += holding.toHTML() + '\r\n'
        html += '</tbody>\r\n'
        html+='</table>\r\n'
        html += '<h4>Total cost: ${0}</h4>\r\n'.format(self.totalCost())
        html += '<h4>Total value: ${0}</h4>\r\n'.format(self.totalValue())
        html += '<h4>Total profit: ${0}</h4>\r\n'.format(self.totalProfit())
        html += '<h4>Day profit: ${0}</h4>\r\n'.format(self.dayProfit())
        html += '<h4>Prices retrieved: {0}</h4>\r\n'.format(self.lastReloadTime)
        html += '<h4>Source: {0}</h4>\r\n'.format(self.source)
                
        return html
    
#A single stock holding
class Holding(object):
    def __init__(self, symbol, name, holding, purchase_price, date, bid=None, offer=None, change=None):
        self.symbol=symbol
        self.name = name
        self.holding=holding
        self.purchase_price = purchase_price
        self.purchase_date = date
        self.bid=bid
        self.offer=offer
        self.change=change
        
    def save(self):
        sql = """insert into holdings (symbol, holding, purchase_price, purchase_date)
                values ('?,?,?,?');"""
        cursor.execute(sql, ( self.symbol, self.holding, self.purchase_price, self.purchase_date))

    #Write holding as a single record to the cache table
    def cache(self):
        sql="insert into cache values(?,?,?,?,?,?,?,?)"
        stockdb.execute(sql, (self.symbol,
                              self.name,
                              self.holding,
                              self.purchase_price,
                              self.purchase_date,
                              self.bid,
                              self.offer,
                              self.change))
    def value(self):
        price=0.0
        try:
            price = float(self.bid)
        except (ValueError, TypeError):
            price=0.0
        return self.holding * price

    def purchaseCost(self):
        try:
            price = float(self.purchase_price)
        except (ValueError, TypeError):
            price=0.0
        return self.holding * price

    def profit(self):
        return self.value() - self.purchaseCost()

    def dayProfit(self):
        try:
            change = float(self.change)
        except (ValueError, TypeError):
            change=0.0
        return self.holding * change
    
    def __unicode__(self):
        return "symbol:{0} holding:{1} bid: {2} offer: {3} change: {4} gain/loss: {8} cost: ${5} value: ${6} profit:${7}".format(self.symbol, 
                                                                  self.holding,
                                                                  self.bid,
                                                                  self.offer,
                                                                  self.change,
                                                                  self.purchaseCost(),
                                                                  self.value(),
                                                                  self.profit(),
                                                                  self.dayProfit())
    
    def __str__(self):
        return self.__unicode__()

    #Return a representation as an HTML table row
    def toHTML(self):
        if float(self.change) >=0.0:
            gainLoss = "gain"
        else:
            gainLoss="loss"
        html = '<tr class="holding">'
        html += '<td>{0}</td>'.format(self.symbol)
        html += '<td>{0}</td>'.format(self.name)
        html += '<td>{0}</td>'.format(self.holding)
        html += '<td>{0}</td>'.format(self.purchase_price)
        html += '<td>{0}</td>'.format(self.bid)
        html += '<td>{0}</td>'.format(self.offer)        
        html += '<td>{0}</td>'.format(self.value())
        html += '<td>{0}</td>'.format(self.profit())    
        html += '<td class="{1}">{0}</td>'.format(self.change, gainLoss)
        html += '<td class="{1}">{0}</td>'.format(self.dayProfit(), gainLoss)    
        html += '</tr>'
        return html


######## Unit tests
class TestHolding(unittest.TestCase):
    def setUp(self):
        self.cursor = stockdb.getCursor()
        self.new_holding = Holding("AFI.AX", 1601, 6.16, "2015-01-02 14:30:00.000")
        self.new_holding.save(self.cursor)
        self.new_holding.cache()
              
    def tearDown(self):
        pass

class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.cursor = stockdb.getCursor()

    def testLoadAll(self):
        holdings = Holdings()
        holdings.loadHoldings()
        self.assertEqual(len(holdings), 6)

    def testAll(self):
        h=getHoldings()
        print h.toHTML()
        
    def tearDown(self):
        pass

class TestTimeUtils(unittest.TestCase):
    def testConfig(self):
        serverOffset = configdb.getConfig('server_utcoffset')
        self.assertEqual(serverOffset, '-0800')

    def testOffsetParser(self):
        self.assertEqual(parseOffset('+0100').seconds, 3600)
        self.assertEqual(parseOffset('-0100').days, -1)
        self.assertEqual(parseOffset('-0100').seconds, 23 * 3600)

    def testToUTC(self):
        d=datetime.datetime(2015, 02, 25, 17, 00, 00)
        self.assertEqual(toUTC(d, '+0000'), d)
        self.assertEqual(toUTC(d, '+0200'), d + datetime.timedelta(hours=-2))
        self.assertEqual(toUTC(d, '-0200'), d + datetime.timedelta(hours=2))
    
if __name__=="__main__":
    unittest.main()
