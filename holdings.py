#!/usr/bin/python

"""
Database accessors for grabbing current holdings
"""

from __future__ import division

import unittest
import datetime
import YahooFinance
import configdb
import stockdb
import stockutils

class HoldingNotFound(Exception):
    pass

class NotSoldException(Exception):
    pass
def getHoldings():
    cursor=stockdb.getCursor()
    holdings=Holdings()
    holdings.load()
    return holdings

#A list of Holding objects 
class Holdings(object):
    def __init__(self):
        self.holdings=[]
        self.lastReloadTime = configdb.getConfig('last_reload')

    #Load holdings from db and get prices from Yahoo!
    def load(self):
        self.holdings=[]
        self.sales=[]
        if self.shouldReload():
            self.loadHoldings()
            self.getPrices()
            self.source = "Yahoo!"
            self.writeToCache()
        else:
            self.loadFromCache()
            self.source="Cache"
    
    #Load all holdings from database
    def loadHoldings(self):
        cursor = stockdb.getCursor()
        sql = """select symbol, holding, purchase_date, purchase_price, sale_date, sale_price
                 from holdings;"""
        cursor.execute(sql)
        for row in cursor:
            holding = Holding(row[0], row[1], row[2], row[3], row[4], row[5])
            if row[4] is None:
                self.holdings.append(holding)
            else:
                self.sales.append(holding)
            
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
        now_str=now.strftime(stockutils.timeFormat)
        configdb.setConfig('last_reload', now_str)

    #Pull holdings and prices from cache table
    def loadFromCache(self):
        cursor = stockdb.getCursor()
        sql = """select symbol,
                        name,
                        holding,
                        purchase_date,
                        purchase_price,
                        sale_date,
                        sale_price,
                        bid,
                        offer,
                        change
                        from cache"""
        cursor.execute(sql)
        for row in cursor:
            holding = Holding(row[0],
                              row[2], #Skip name for now
                              row[3],
                              row[4],
                              row[5],
                              row[6])
            holding.name = row[1]
            holding.bid=row[7]
            holding.offer=row[8]
            holding.change=row[9]
            if row[5] is None: #Skip sold shares
                self.holdings.append(holding)
            else:
                self.sales.append(holding)    

    #Clear and re-populate cache table
    def writeToCache(self):
        stockdb.executeDirect('delete from cache')
        for holding in self.holdings:
            holding.cache()
        for sale in self.sales:
            sale.cache()
    
    #Should we reload yet?
    def shouldReload(self):
        now = datetime.datetime.now()
        return (self.lastReload() + self.minReload()) < now

    #When did we last hit Yahoo!?
    def lastReload(self):
        str_time = configdb.getConfig('last_reload')
        #Parse the datetime
        return datetime.datetime.strptime(str_time, stockutils.timeFormat)

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
        return sum([holding.profit() for holding in self.holdings]) + sum([sale.profit() for sale in self.sales])
    
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

    def salesTable(self):
        html = """
        <h3>Sales</h3>
        <table class="holdings">\r\n
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Purchase cost</th>
            <th>Sale Value</th>
            <th>Gain/Loss</th>
            <th>Purchase date</th>
            <th>Sale Date</th>
            <th>Annualized return</th>
          </tr>
        </thead>
        <tbody>"""
        for sale in self.sales:
            html += """
            <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{:.2%}</td></tr>
            """.format(sale.symbol, 
                       sale.purchaseCost(), 
                       sale.saleValue(),
                       sale.profit(),
                       stockutils.toDDMMYYYY(sale.purchase_date),
                       stockutils.toDDMMYYYY(sale.sale_date),
                       sale.annualizedReturn())
        html += """
        </tbody>
        </table>
        """
        return html
    
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
        html += self.salesTable()
        html += '<h4>Total cost: ${0}</h4>\r\n'.format(self.totalCost())
        html += '<h4>Total value: ${0}</h4>\r\n'.format(self.totalValue())
        html += '<h3>Growth: {:.02%}</h3>\r\n'.format(self.totalProfit()/self.totalCost())
        html += '<h4>Total profit: ${0}</h4>\r\n'.format(self.totalProfit())
        html += '<h4>Day profit: ${0}</h4>\r\n'.format(self.dayProfit())
        html += '<h4>Prices retrieved: {0}</h4>\r\n'.format(self.lastReloadTime)
        html += '<h4>Source: {0}</h4>\r\n'.format(self.source)
                
        return html
    
#A single stock holding
class Holding(object):

    def __init__(self, 
                 symbol, 
                 holding, 
                 purchase_date, 
                 purchase_price, 
                 sale_date=None,
                 sale_price=None,
                 id=None):
        self.symbol=symbol
        self.holding=holding
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date
        self.sale_price = sale_price
        self.sale_date = sale_date
        self.bid = 0.0
        self.offer = 0.0
        self.change= 0.0
        self.id=id
        self.name="Not loaded"

    @classmethod
    def findById(cls, key):
        sql = """
        select
        id,
        symbol,
        holding,
        purchase_price,
        purchase_date,
        sale_price, 
        sale_date
        from holdings
        where id=?;"""
        sql="select * from holdings where id=?"
        cursor = stockdb.getCursor()
        cursor.execute(sql, (key,)) #The sqlite api interprets 100 as 1,0,0 unless you put this trailing comma on
        r=cursor.fetchone()
        if r is not None:
            return Holding(r[1],r[2],r[3],r[4],r[5],r[6],r[0])
        else:
            raise HoldingNotFound("No holding with id {} in database".format(key))
    
    def save(self):
        if self.id is None:
            sql = """insert into holdings (symbol, holding, 
            purchase_price, purchase_date, 
            sale_price, sale_date) 
            values (?,?,?,?,?,?);"""
            stockdb.execute(sql, (self.symbol,
                                  self.holding, 
                                  self.purchase_price, 
                                  self.purchase_date,
                                  self.sale_price,
                                  self.sale_date))
        else:
            sql = """
            update holdings set 
            symbol = ?,
            holding=?,
            purchase_price=?,
            purchase_date=?,
            sale_price=?,
            sale_date=?
            where id = ?
            """
            stockdb.execute(sql, (self.symbol,
                                  self.holding, 
                                  self.purchase_price, 
                                  self.purchase_date,
                                  self.sale_price,
                                  self.sale_date,
                                  self.id))

    #Write holding as a single record to the cache table
    def cache(self):
        sql="""insert into cache(
                symbol,
                name,
                holding,
                purchase_price,
                purchase_date,
                sale_price,
                sale_date,
                bid,
                offer,
                change)
                values(?,?,?,?,?,?,?,?,?,?)"""
        stockdb.execute(sql, (self.symbol,
                              self.name,
                              self.holding,
                              self.purchase_price,
                              self.purchase_date,
                              self.sale_price,
                              self.sale_date,
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

    def sold(self):
        return self.sale_date is not None
    
    def holdDuration(self):
        if self.sold():
            return stockutils.dateFromString(self.sale_date) - stockutils.dateFromString(self.purchase_date)
        else:
            raise NotSoldException("{} has not been sold".format(self.symbol))
                                   
    def saleValue(self):
        if self.sold():
            return self.sale_price * self.holding
        else: 
            raise NotSoldException("{} has not been sold".format(self.symbol))
    
    def profit(self):
        if self.sold():
            return self.saleValue() - self.purchaseCost()
        else:
            return self.value() - self.purchaseCost()

    def annualizedReturn(self):
        return annualizedReturn(self.purchaseCost(), self.saleValue(), self.holdDuration().days)
    
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
        try:
            if float(self.change) >=0.0:
                gainLoss = "gain"
            else:
                gainLoss="loss"
        except ValueError:
            gainLoss = "gain"
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

class HoldingSummary(object):
    def __init__(self, h):
        self.symbol=h.symbol
        self.holding=h.holding
        self.purchase_cost=h.purchaseCost()
        self.value=h.value()
        
    def addHolding(self, h):
        self.holding += h.holding
        self.purchase_cost += h.purchase_price * h.holding

    def toHTML(self):
        if self.value >= self.purchase_cost:
            gainLoss = "gain"
        else:
            gainLoss = "loss"
        return """
            <tr>
                      <td>{}</td>
                      <td>{}</td>
                      <td>{}</td>
                      <td class="{}">{}</td>
                      <td>{}</td>
                  </tr>\r\n""".format(self.symbol,
                                      self.holding,
                                      self.purchase_cost,
                                      gainLoss,
                                      self.value,
                                      self.growth_percentage())
    def growth_percentage(self):
        try:
            growth = (self.value - self.purchase_cost)/self.purchase_cost
        except ZeroDivisionError:
            return "n/a:"
        return "{:.2%}".format(growth)

class PortfolioSummary(object):
    def __init__(self, holdings):
        self._summary={}
        self._holdings = holdings
        for h in self._holdings:
            if self._summary.has_key(h.symbol):
                self._summary[h.symbol].addHolding(h)
            else:
                self._summary[h.symbol] = HoldingSummary(h)
    def summary(self):
        return self._summary
    def toHTML(self):
        html="""
        <table>
          <tr><th>Symbol</th><th>Holding</th><th>Cost</th><th>Value</th><th>Gain</th></tr>\r\n"""
        for k in self._summary:
            html += self._summary[k].toHTML()
        html += "</table>"
        html += '<h4>Total cost: ${0}</h4>\r\n'.format(self._holdings.totalCost())
        html += '<h4>Total value: ${0}</h4>\r\n'.format(self._holdings.totalValue())
        html += '<h4>Total profit: ${0}</h4>\r\n'.format(self._holdings.totalProfit())
        html += '<h3>Growth: {:.02%}</h3>\r\n'.format(self._holdings.totalProfit()/self._holdings.totalCost())
        html += '<h4>Day profit: ${0}</h4>\r\n'.format(self._holdings.dayProfit())
        html += '<h4>Prices retrieved: {0}</h4>\r\n'.format(self._holdings.lastReloadTime)
        html += '<h4>Source: {0}</h4>\r\n'.format(self._holdings.source)
        return html

######## Unit tests
class TestHolding(unittest.TestCase):
    def setUp(self):
        self.cursor = stockdb.getCursor()
        self.new_holding = Holding("AFI.AX", "AFI FPO", 1601, 6.16, "2015-01-02 14:30:00.000")
        self.new_holding.save(self.cursor)
        self.new_holding.cache()
              
    def tearDown(self):
        pass

class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.cursor = stockdb.getCursor()

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
        self.assertEqual(stockutils.parseOffset('+0100').seconds, 3600)
        self.assertEqual(stockutils.parseOffset('-0100').days, -1)
        self.assertEqual(stockutils.parseOffset('-0100').seconds, 23 * 3600)

    def testToUTC(self):
        d=datetime.datetime(2015, 02, 25, 17, 00, 00)
        self.assertEqual(stockutils.toUTC(d, '+0000'), d)
        self.assertEqual(stockutils.toUTC(d, '+0200'), d + datetime.timedelta(hours=-2))
        self.assertEqual(stockutils.toUTC(d, '-0200'), d + datetime.timedelta(hours=2))

def annualizedReturn(initialCapital,
                     finalCapital,
                     duration): #Duration is in days, 365.25 per year
    if initialCapital == 0:
        #FIXME - this needs a group by in the select. What's the annualized return on a dividend payment?
        return 0.0
    years = duration / 365.25
    return ((finalCapital/initialCapital) ** (1/years)) - 1.0

#class testAnnualizedReturn(unittest.TestCase):
#    def testAnnualizedReturn(self):
#        self.assertEqual(annualizedReturn (100.0, 100.0, 100), 0.0)

class testSummaries(unittest.TestCase):
    def setUp(self):
        self.new_holding = Holding("AFI.AX", 1601, 6.16, "2015-01-02 14:30:00.000")
        
    def testInit(self):
        s = HoldingSummary(self.new_holding)
        self.assertEqual(s.symbol, "AFI.AX")

class testPortfolioSummary(unittest.TestCase):
    
    def testPortfolio(self):
        s = PortfolioSummary(getHoldings())
        print s
        
if __name__=="__main__":
    unittest.main()
