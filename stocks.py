#!/usr/bin/python

import cgi
import cgitb

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
    b="""
        <body>
            <h4>Stocks</h4>
        </body>
    </html>"""
    return b

def page():
    return contentType() + header() + body()

print page()

