#!/usr/bin/python

import httpproxy
import urllib2
import json
import httplib
import asxhttp

USEPROXY=False
if USEPROXY:
    host='isaproxy'
    port=89
    user='######'
    #This caches the proxy data with the users password
    httplib==httpproxy.HTTPProxy(host, port, user).getUrlLib()
else:
    httplib=urllib2

"""
quote='{"data":[{"code":"SUN","close_date":"2017-11-06T00:00:00+1100","close_price":13.88,"change_price":0.02,"volume":1620108,"day_high_price":13.94,"day_low_price":13.82,"change_in_percent":"0.144%"}]}'
"""

class Quote:
    cache = {}
    
    def __init__(self, symbol, lib=httplib):
        self.symbol=symbol
        self.lib=lib
        self.priceData=None
        self.retrieved=False
        self._getPrice()

    """This is the service-specific bit"""
    def _getPrice(self):
        if Quote.cache.has_key(self.symbol):
            self.close_price = Quote.cache[self.symbol]
            #print("Retreived {}:{} from cache".format(self.symbol, self.close_price))
        else:
            price=asxhttp.getStock(self.symbol)
            self.close_price=price
            Quote.cache[self.symbol]=self.close_price
            #print("Retreived {}:{} from ASX".format(self.symbol, self.close_price))
        self.change_price=0.0
        
    #_getPrice_JSON worked with the old, undocumented data feed from ASK
    def _getPrice_JSON(self):
        if not self.retrieved:
            url='http://data.asx.com.au/data/1/share/{}/prices?interval=daily&count=1'.format(self.symbol)
            try:
                conn=self.lib.urlopen(url)
                priceData=json.load(conn)
                raw=priceData['data'][0]
                self.close_date=raw['close_date']
                self.close_price=raw['close_price']
                self.change_in_percent=raw['change_in_percent']
                self.day_low_price=raw['day_low_price']
                self.volume=raw['volume']
                self.change_price=raw['change_price']
                self.day_high_price=raw['day_high_price']
                self.code=raw['code']
                self.retrieved=True
            except Exception:
                raise
    def __str__(self):
        if self.retrieved:
            s="{}: {}".format(self.code,
                              self.close_price)
        else:
            s="{}: Not retrieved".format(self.symbol)

        return s

