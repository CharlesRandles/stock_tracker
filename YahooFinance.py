#!/usr/bin/python

"""
Utilities for retrieving stock data from Yahoo
See https://code.google.com/p/yahoo-finance-managed/wiki/csvQuotesDownload
"""

"""Stores a single stock quote"""
class Quote(object):
    def __init__(self, symbol):
        self.symbol = symbol

import urllib2
"""
Class to retrieve a set of quotes from Yahoo and parse them into Quote objects
"""
class YahooQuotes(object):
    def __init__(self, symbols):
        self.quotes = {}
        self.buildQuotes(symbols)

    #Get the data, parse it and build the quote list
    def buildQuotes(self, symbols):
        rawQuotes = self.getQuotesFromYahoo(symbols).split("\r\n")
        for line in rawQuotes:
            data = line.split(',')
            quote = Quote(data[1].strip('"'))
            quote.name = data[0].strip('"')
            quote.offer = data[3]
            quote.bid = data[2]
            quote.peak = data[4]
            quote.change = data[5]
            self.quotes[quote.symbol]=quote
            
    #Retrieve .csv data from Yahoo!
    def getQuotesFromYahoo(self, symbols):
        options = [  'n'
                    ,'s'
                    ,'l1'
                    ,'o'
                    ,'p'
                    ,'c1']
        url = YahooCSVURL(symbols, options).url
        response = urllib2.urlopen(url)
        return response.read().strip() #delete trailing line


    def __getitem__(self, key):
        return self.quotes[key]
    
    def __len__(self):
        return len(self.quotes)
    
"""
Class to build a URL for Yahoo stock quotes
"""
class YahooCSVURL(object):
    """
    Takes a list of stocks and creates a URL to the Yahoo! API that will
    download them as .csv
    Example URL for CTN.AX: "http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv"
    """
    def __init__(self, stockList, options):
        quotesURL="http://download.finance.yahoo.com/d/quotes.csv"
        queryString = ",".join(stockList)
        optionString = ''.join(options)
        options = "&f={0}&e=.csv".format(optionString)
        self.url = quotesURL + "?s=" + queryString + options

    def __unicode__(self):
        return self.url
    def __str__(self):
        return __unicode__(self)

import unittest
    
class TestURLs(unittest.TestCase):
    def setUp(self):
        self.options = [ 'n'
                        ,'s'
                        ,'l1'
                        ,'o'
                        ,'p']
                      #,'c1'
        
    def testSingleStock(self):
        stock = ["CTN.AX"]
        url = YahooCSVURL(stock, self.options)
        self.assertEqual(url.url, "http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv")
    def testMultipleStock(self):
        stock = ["CTN.AX", "MPL.AX"]
        url = YahooCSVURL(stock, self.options)
        self.assertEqual(url.url, "http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX,MPL.AX&f=nsl1op&e=.csv")
    
class TestQuotes(unittest.TestCase):
    def testQuotes(self):
        symbols = ['CTN.AX']
        quotes = YahooQuotes(symbols)
        self.assertEqual(len(symbols), 1)
        self.assertEqual(quotes[symbols[0]].symbol, symbols[0]) #Should get the symbol we asked for

# http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv
#'http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv'
        
if __name__=="__main__":
    unittest.main()
