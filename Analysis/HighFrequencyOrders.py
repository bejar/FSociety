"""
.. module:: HighFrequencyOrders

HighFrequencyOrders
*************

:Description: HighFrequencyOrders

    

:Authors: bejar
    

:Version: 

:Created on: 20/02/2019 13:21 

"""

import argparse

import gzip

import numpy as np


from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter
from FSociety.Config import datapath, ITCH_days


__author__ = 'bejar'



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')
    parser.add_argument('--day', help="dia del anyo", type=int, default=0)
    parser.add_argument('--stock', help="Stock del analisis", default='GOOGL')

    args = parser.parse_args()
    year = args.year
    stock = args.stock
    day = args.day


    # if 'G' in year:
    #     datapath = datapath + '/GIS/'

    rfile = ITCHMessages(year, day, stock)
    rfile.open()
    sorders = OrdersProcessor(history=True)

    for order in rfile.get_order():
        # print(order.to_string())
        sorders.insert_order(order)

    sorders.list_executed(mode='exec', hft=True)