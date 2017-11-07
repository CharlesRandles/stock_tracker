#!/usr/bin/python

import ASXQuote

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
    q=ASXQuote.Quote(stock)
    print(str(q))
