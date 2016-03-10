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
    <form method="GET" action="summary.py">
        <input type="submit" value="Refresh" />
    </form>
    """
    return f

def body():
    stocks=holdings.PortfolioSummary(holdings.getHoldings())
    b="""
    <body>
        <h4>Stocks</h4>
        {0}
        {1}
        <a href="stocks.py">Full Report</a>
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




