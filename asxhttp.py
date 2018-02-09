#!/usr/bin/python

import httplib
from HTMLParser import HTMLParser

ASX_SERVER='www.asx.com.au'
ASX_URL='/asx/markets/priceLookup.do?by=asxCodes&asxCodes={}'

SCANNING=0
LAST_PRICE=1

class ASXParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.state=SCANNING
        self.last_price = None
        
    def handle_starttag(self, tag, attrs):
        if tag=='td':
            if len(attrs)>0:
                key,val=attrs[0]
                if key=='class' and val=='last':
                    print "Wheee!"
                    #Found the data we want
                    self.state=LAST_PRICE

    def handle_data(self, data):
        if self.state==LAST_PRICE:
            self.state=SCANNING
            self.last_price=data.strip()

def retrieveStockPage(symbol):
    url=ASX_URL.format(symbol)
    conn=httplib.HTTPSConnection(ASX_SERVER)
    conn.request('GET', url)
    response = conn.getresponse()
    #print "Status: {} {}".format(response.status, response.reason)
    page = response.read()
    return page


def getStock(symbol):
    page=retrieveStockPage(symbol)
    parser=ASXParser()
    parser.feed(page)
    print "Symbol: {} Last Price: {}".format(symbol, parser.last_price)
    return parser.last_price
