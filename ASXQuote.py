#!/usr/bin/python

import httpproxy
import json

host='isaproxy'
port=89
user='U335449'

quote='{"data":[{"code":"SUN","close_date":"2017-11-06T00:00:00+1100","close_price":13.88,"change_price":0.02,"volume":1620108,"day_high_price":13.94,"day_low_price":13.82,"change_in_percent":"0.144%"}]}'

#This caches the proxy data with the users password
proxyLib=httpproxy.HTTPProxy(host, port, user).getUrlLib()

class Quote:
    def __init__(self, symbol, lib=proxyLib):
        self.symbol=symbol
        self.lib=lib
        self.priceData=None
        self.retrieved=False
        self._getPrice()

    """This is the service-specific bit"""
    def _getPrice(self):
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

        
