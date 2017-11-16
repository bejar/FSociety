"""
.. module:: ExecuteStock

ExecuteStock
*************

:Description: ExecuteStock

    

:Authors: bejar
    

:Version: 

:Created on: 14/11/2017 11:10 

"""

import argparse

import gzip

import numpy as np


from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company
from FSociety.Config import datapath, ITCH_days


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

    for order in rfile.get_order():
        print(order.to_string())
        sorders.insert_order(order)

        # data = mess.split(',')
        # timestamp = ITCHtime(int(data[1].strip()))
        # order = data[2].strip()
        # ORN = data[3].strip()
        # if order in ['F', 'A']:
        #     if order == 'A':
        #         price = float(data[7].strip())
        #     else:
        #         price = float(data[8].strip())
        #     sorders.process_order(stock, order, ORN, otime=timestamp.itime, bos=data[5].strip(), size=int(data[6].strip()), price=price)
        #
        # if order == 'U':
        #     nORN = data[4].strip()
        #     sorders.process_order(stock, order, nORN, otime=timestamp.itime, updid=ORN, size=int(data[5].strip()), price=float(data[6].strip()))
        #
        # if order == 'D':
        #     sorders.process_order(stock, order, ORN)
        #
        # if order == 'X':
        #     sorders.process_order(stock, order, ORN, size=int(data[4]))
        #
        # if order == 'E':
        #     sorders.process_order(stock, order, ORN, otime=timestamp.itime, size=int(data[4]))
        #
        # if order == 'C':
        #     sorders.process_order(stock, order, ORN, otime=timestamp.itime, size=int(data[4]), price=float(data[6].strip()))


    sorders.list_executed(mode='exec')


