#!/usr/bin/python

"""Script to record buying, selling and unselling of shares"""

import sys

import stockdb
import stockutils
import holdings
import YahooFinance

class UnknownCommand(Exception):
    pass

#Action functions
def show(*args):
    print "show: {}".format(*args) 
    cursor = stockdb.getCursor()
    sql = """select id, symbol, holding, sale_price from holdings"""
    cursor.execute(sql)
    for row in cursor:
        print("{}\t{}\t{}\t{}".format(row[0],
                                      row[1],
                                      row[2],
                                      row[3]))
def buy(*args):
    symbol = args[0][0]
    print("Looking up {}...".format(symbol)) 
    name = YahooFinance.checkName(symbol)
    if name == None:
        print("{} is not a valid stock symbol".format(symbol))
        return
    qty = args[0][1]
    purchase_price = args[0][2]
    purchase_date = stockutils.nowUTC()
    if confirmAction("Buy {} of {} ({}) at ${} ?".format(qty,
                                                   symbol,
                                                   name,
                                                   purchase_price)):
        newHolding = holdings.Holding(symbol=symbol,
                                    holding=qty, 
                                    purchase_price=purchase_price, 
                                    purchase_date=purchase_date)
        newHolding.save()
        show(*args)

def sell(*args):
    print "sell: {}".format(*args)
    key = args[0][0]
    price = args[0][1]
    print "Selling {} at {}".format(key, price)
    try:
        holding = holdings.Holding.findById(key)
        holding.sale_date=stockutils.nowUTC()
        holding.sale_price = price
        if confirmAction("Sell all of {}, bought at {} for {} ?".format(holding.symbol,
                                                                        holding.purchase_price,
                                                                        price)):
            holding.save()
            show(*args)
        else:
            print("Not sold")
    except holdings.HoldingNotFound:
        print("No holding with id {} found in database".format(key))

              
def unsell(*args):
    print "unsell: {}".format(*args) 
    key = args[0][0]
    print "Unselling {}".format(key)
    try:
        holding = holdings.Holding.findById(key)
        if confirmAction("Unsell all of {}, sold for {} on {} ?".format(holding.symbol,
                                                                        holding.sale_price,
                                                                        holding.sale_date)):
            holding.sale_price = None
            holding.sale_date = None
            holding.save()
            show(*args)
        else:
            print("Not unsold")
    except holdings.HoldingNotFound:
        print("No holding with id {} found in database".format(key))

def delete(*args):
    print "delete: {}".format(*args) 
    raise Exception("delete not implemented")

def parseArgs(argv):
    commands = ['show', 'buy', 'sell', 'unsell', 'delete']
    command = 'unrecognised'
    if argv[0] in commands:
        return argv[0], argv[1:]
    else:
        raise UnknownCommand("{} is not a recognised command".format(argv[0]))

def confirmAction(prompt):
    answer = raw_input(prompt)
    return answer[0] in ['y','Y']

def usage():
    usageStr =  "manage.py cmd options\n"
    usageStr += "\twhere cmd is [show|buy|sell|unsell|delete]\n"
    usageStr += "\tmanage show\n"
    usageStr += "\tmanage buy {symbol} {quantity} {price}\n"
    usageStr += "\tmanage sell {id} {price}\n"
    usageStr += "\tmanage unsell {id}\n"
    usageStr += "\tmanage delete {id}\n"
    print(usageStr)
    
def main():
    if len(sys.argv) < 2:
        usage()
        return
    action, args = parseArgs(sys.argv[1:])
    actions = {'show': show,
               'buy' :buy,
               'sell' : sell,
               'unsell' : unsell,
               'delete' : delete}
    try:
        actionFn = actions[action]
        actionFn(args)
    except KeyError:
        usage()

if __name__=="__main__":
    main()
