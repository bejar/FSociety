"""
.. module:: Executions

Executions
*************

:Description: Executions

    

:Authors: bejar
    

:Version: 

:Created on: 30/09/2016 12:37 

"""


from FSociety.Util import datapath, StockOrders, ITCH_days, Company
import argparse


__author__ = 'bejar'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default=None)
    parser.add_argument('--day', help="nuemro de dia del anyo a analizar", default=None)
    parser.add_argument('--stock', help="Ticker a analizar", default=None)

    args = parser.parse_args()
    year = args.year
    stock = args.stock
    nday = int(args.day)

    day = ITCH_days[year][nday]
    sorders = StockOrders()
    cpny = Company()
    rfile = open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv', 'r')
    wfile = open(datapath + '/Results/' + day + '-' + stock + '-EXEC.csv', 'w')

    i = 0
    norders = 0
    for mess in rfile:
        data = mess.split(',')
        timestamp = int(data[1].strip())
        order = data[2].strip()
        ORN = data[3].strip()
        if order in ['F', 'A']:
            if order == 'A':
                price = float(data[7].strip())
            else:
                price = float(data[8].strip())
            sorders.insert_order(stock, order, ORN, otime=timestamp, bos=data[5].strip(), price=price)
            norders += 1
        if order == 'U':
            nORN =  data[4].strip()
            sorders.insert_order(stock, order, nORN, timestamp, updid=ORN, price=data[6].strip())
        # Computes the time between placing and order and canceling it
        if order == 'D':
            trans = sorders.query_id(ORN)
            sorders.insert_order(stock, order, ORN)
        # Computes the time between placing and order and its execution
        if order in ['E', 'C']:
            trans = sorders.query_id(ORN)
            wfile.write(stock + ',' + str(timestamp) + ',' + data[4].strip() + ',' + str(trans[1]) + ',' + trans[2] + ',' + str(trans[3]))

            if order == 'C':
                 wfile.write(',' + str(data[6].strip()) + '\n')
            else:
                 wfile.write('\n')

        i += 1
        if i % 10000 == 0:
            print('.', end='', flush=True)
            wfile.flush()

    wfile.close()
    rfile.close()