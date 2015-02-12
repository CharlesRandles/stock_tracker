#!/usr/bin/python

import cgi
import cgitb

cgitb.enable()

def header():
    h="""
    <html>
        <head>
            <title>Stocks</title>
        </head>"""
    return h

def body():
    b="""
        <body>
            <h4>Stocks</h4>
        </body>
    </html>"""
    return b

def page():
    return header() + body()

print page()

