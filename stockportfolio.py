#!/usr/bin/python

import stockquote

stocks=['AFI',
        'ARG',
        'CTN',
        'GEM',
        'GRB',
        'IPH',
        'RFG',
        'SUN',
        'TLS',
        'VAE',
        'VAP',
        'VAS',
        'VGS',
        'VTS',
        'YBR']

for stock in stocks:
    q=stockquote.Quote(stock)
    print(str(q))
