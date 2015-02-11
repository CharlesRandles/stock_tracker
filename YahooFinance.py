#!/usr/bin/python

"""
Utilities for retrieving stock data from Yahoo
See https://code.google.com/p/yahoo-finance-managed/wiki/csvQuotesDownload
"""

import unittest

"""
Class to build a URL for Yahoo stock quotes
"""
class YahooCSVURL(object):
    """
    Takes a list of stocks and creates a URL to the Yahoo! API that will
    download them as .csv
    Example URL for CTN.AX: "http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv"
    """
    def __init__(self, stockList):
        quotesURL="http://download.finance.yahoo.com/d/quotes.csv"
        queryString = ",".join(stockList)
        options = "&f=nsl1op&e=.csv"
        self.url = quotesURL + "?s=" + queryString + options

    def __unicode__(self):
        return self.url
    def __str__(self):
        return __unicode__(self)
    
class TestURLs(unittest.TestCase):
    def testSingleStock(self):
        stock = ["CTN.AX"]
        url = YahooCSVURL(stock)
        self.assertEqual(url.url, "http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv")
    def testMultipleStock(self):
        stock = ["CTN.AX", "MPL.AX"]
        url = YahooCSVURL(stock)
        self.assertEqual(url.url, "http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX,MPL.AX&f=nsl1op&e=.csv")
    
        
        # http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv

#'http://download.finance.yahoo.com/d/quotes.csv?s=CTN.AX&f=nsl1op&e=.csv'
        
if __name__=="__main__":
    unittest.main()
