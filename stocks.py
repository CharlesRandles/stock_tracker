#!/usr/bin/python

import cgi
import cgitb
import holdings
import unittest
import configdb

cgitb.enable()

DB='db/holdings.db'

#########  HTML Genaration ###############
def contentType():
    ct="""Content-type: text/html

    """
    return ct

def header():
    h="""
    <html>
        <head>
            <title>Stocks</title>
            <link rel="stylesheet" href="stocks.css"/>
        </head>"""
    return h

def body():
    stocks=holdings.getHoldings()
    b="""
        <body>
            <h4>Stocks</h4>
            {0}
        </body>
    </html>""".format(stocks.toHTML())
    return b

def page():
    return contentType() + header() + body()

########## End HTML Generation ###############
 
#Generate html
print page()




