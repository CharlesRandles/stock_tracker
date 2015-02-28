#!/usr/bin/python
"""
Helper fns for HTML generation
"""
def contentType():
    ct="""Content-Type: text/html; charset=utf-8

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
