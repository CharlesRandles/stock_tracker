#!/usr/bin/python

import cgi
import cgitb
import holdings
import unittest
import configdb

cgitb.enable()

DB='db/holdings.db'

#########  HTML Generation ###############
def contentType():
    ct="""Content-type: text/html

    """
    return ct

def header():
    h="""
<!DOCTYPE html>
<html>
    <head>
        <title>Stocks</title>
        <link rel="stylesheet" href="stocks.css"/>
    </head>"""
    return h

def refresh_form():
    f="""
    <form method="GET" action="stocks.py">
        <input type="submit" value="Refresh" />
    </form>
    """
    return f

def body():
    stocks=holdings.getHoldings()
    b="""
    <body>
        <h4>Stocks</h4>
        {0}
        {1}
    </body>
</html>
    """.format(stocks.toHTML(),
                      refresh_form())
    return b

def page():
    return contentType() + header() + body()

########## End HTML Generation ###############
 
#Generate html
print page()




