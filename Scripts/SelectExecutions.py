"""
.. module:: Executions

Executions
*************

:Description: Executions

    

:Authors: bejar
    

:Version: 

:Created on: 30/09/2016 12:37 

"""

from FSociety.Data import Company, OrdersProcessor
from FSociety.Config import datapath, ITCH_days
from FSociety.ITCH import ITCHMessages

import argparse
import gzip

__author__ = 'bejar'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='')
    parser.add_argument('--day', help="dia del anyo", default='')
    parser.add_argument('--stock', help="Stock del analisis", default='')

    args = parser.parse_args()
    year = str(args.year)
    stock = args.stock

    if year == '':
        year = '2017G'

    if args.day == '':
        day = 0
    else:
        day = int(args.day)

    if stock == '':
        stock = 'AAPL'

    if 'G' in year:
        datapath = datapath + '/GIS/'

    rfile = ITCHMessages(year, day, stock)
    sorders = OrdersProcessor()
    rfile.open()

    cpny = Company()

    wfile = open(datapath + '/Results/' + day + '-' + stock + '-EXEC.csv', 'w')

    i = 0
    norders = 0
    for order in rfile.get_order():
        print(order.to_string())
        sorders.insert_order(order)
        if order.type in ['E', 'C']:
            trans = sorders.query_id(order.ORN)
            wfile.write(stock + ',' + str(order.otimes) + ',' + str(trans.otime) + ',' + trans.buy_sell + ',' + str(order.size) + ',' + str(trans.price))

            if order == 'C':
                 wfile.write(',' + str(order.price) + '\n')
            else:
                 wfile.write('\n')

        i += 1
        if i % 10000 == 0:
            print('.', end='', flush=True)
            wfile.flush()

    wfile.close()
    rfile.close()

    # for mess in rfile:
    #     data = mess.split('&')
    #     timestamp = int(data[1].strip())
    #     order = data[2].strip()
    #     ORN = data[3].strip()
    #     if order in ['F', 'A']:
    #         price = float(data[7].strip())
    #         sorders.process_order(stock, order, ORN, otime=timestamp.itime, bos=data[5].strip(), price=price)
    #         # norders += 1
    #     if order == 'U':
    #         nORN =  data[4].strip()
    #         sorders.process_order(stock, order, nORN, timestamp.itime, updid=ORN, price=data[6].strip())
    #     # Computes the time between placing and order and canceling it
    #     if order == 'D':
    #         trans = sorders.query_id(ORN)
    #         sorders.process_order(stock, order, ORN)
    #     # Computes the time between placing and order and its execution
    #     if order in ['E', 'C']:
    #         trans = sorders.query_id(ORN)
    #         wfile.write(stock + ',' + str(timestamp) + ',' + data[4].strip() + ',' + str(trans.otime) + ',' + trans.buy_sell + ',' + str(trans.price))
    #
    #         if order == 'C':
    #              wfile.write(',' + str(data[6].strip()) + '\n')
    #         else:
    #              wfile.write('\n')
    #
    #     i += 1
    #     if i % 10000 == 0:
    #         print('.', end='', flush=True)
    #         wfile.flush()
    #
    # wfile.close()
    # rfile.close()