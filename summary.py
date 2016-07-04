#!/usr/bin/python

import cgi
import cgitb
import holdings
import unittest
import configdb
import html
import stockdb

cgitb.enable()

#########  HTML Generation ###############
def refresh_form():
    f="""
    <form method="GET" action="summary.py">
        <input type="submit" value="Refresh" />
    </form>
    """
    return f

def groupSummary():
    sql= """select symbol, 
       sum(holding), 
       sum(holding * purchase_price) as paid,
       sum(offer * holding) as value
       from cache
       group by symbol
       order by symbol;"""
    s="<p><table>"
    cursor = stockdb.getCursor()
    cursor.execute(sql,())
    for r in cursor:
        s += "<tr>{}<td>{}</td><td>{}</td><td>{}</td></tr>".format(r[0], r[1], r[2], r[3])
    s += "</table>/p>"
    return s
       

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
    b += groupSummary()
    return b

def page():
    return html.contentType() + html.header() + body()

########## End HTML Generation ###############
 
#Generate html
print page()
