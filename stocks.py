#!/usr/bin/python

import cgi
import cgitb
import holdings
import unittest
import configdb
import html

cgitb.enable()

#########  HTML Generation ###############
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
        <a href="summary.py">Summary Report</a>
    </body>
</html>
    """.format(stocks.toHTML(),
                      refresh_form())
    return b

def page():
    return html.contentType() + html.header() + body()

########## End HTML Generation ###############
 
#Generate html
print page()




