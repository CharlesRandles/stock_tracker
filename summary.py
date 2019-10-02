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
    sql= """select 
       symbol, 
       sum(holding), 
       sum(holding * purchase_price) as paid,
       sum(offer * holding) as value
       from cache
       where sale_date is null
       group by symbol
       order by symbol;"""
    s="<p><table><thead><th>Symbol</th><th>Holding</th><th>Purchase Cost</th><th>Value</th><th>Gain</th></thead>"
    cursor = stockdb.getCursor()
    cursor.execute(sql,())
    for r in cursor:
        try:
            cost = float(r[2])
            value = float(r[3])
            pct_change = ((value - cost) / cost)
        except TypeError:
            cost=r[2]
            value=r[3]
            pct_change="Error."
        colour = "loss"
        try:
            if value > cost:
                colour = "gain"
        except ValueError:
            pass
        s += "<tr><td class={}>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{:.2%}</td></tr>".format(colour, r[0], r[1], cost, value , pct_change)
    s += "</table></p>"
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
    """.format(groupSummary(),
                      refresh_form())
    return b

def page():
    return html.contentType() + html.header() + body()

########## End HTML Generation ###############
 
#Generate html
print page()
