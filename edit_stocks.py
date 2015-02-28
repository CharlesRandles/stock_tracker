#!/usr/bin/python
import cgi
import cgitb
import unittest
import configdb
import holdings
import html

cgitb.enable()

#Table of HTML forms for editing stock holdings
def holdingsForm():
    stocks=holdings.Holdings()
    stocks.loadHoldings()
    html=""
    for stock in stocks:
        html += '<tr>'
        html += "<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td>".format(stock.symbol,
                                                                                      stock.name,
                                                                                      stock.holding,
                                                                                      stock.purchase_date,
                                                                                      stock.purchase_price)
        html += "</tr>\r\n"
    return html
    
def body():
    return """
<body>
<table>
<thead>
<th>Symbol</th>
<th>Name</th>
<th>Shares</th>
<th>Date Purchased</th>
<th>Purchase Price</th>
</thead>
{0}
</table>
</body>
</html>
""".format(holdingsForm())

def page():
    return html.contentType() + html.header() + body()

print page()
