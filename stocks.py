#!/usr/bin/python

import cgi
import cgitb
import holdings

cgitb.enable()

def contentType():
    ct="""Content-type: text/html

    """
    return ct

def header():
    h="""
    <html>
        <head>
            <title>Stocks</title>
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

print page()

