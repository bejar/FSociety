"""
.. module:: Stocks

Stocks
*************

:Description: Stocks

    

:Authors: bejar
    

:Version: 

:Created on: 05/09/2016 12:04 

"""

__author__ = 'bejar'


from ITCHbin import ITCHv5
from ITCHtime import ITCHtime
from ITCHRecord import ITCHRecord
from Util import now
import pandas as pd

pd.__version__ = '0.18'
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from Constants import ITCH_files, datapath, NASDAQ_actions
from Company import Company
from StockOrders import StockOrders

__author__ = 'bejar'


if __name__ == '__main__':
    filename = ITCH_files[2]
    now()
    i= 0

    dataset = ITCHv5(datapath + filename)
    gendata = dataset.records()
    stockdic = {}
    print(filename)

    file = './Data/stockselected.csv'


    rfile = open(file, 'r')
    sstocks = set()
    for stock in rfile:
        sstocks.add(stock.strip())
    rfile.close()

    # print(sstocks)

    dname = filename.split('.')[0]
    wfile = open(datapath + '/Results/' + dname + '-STOCK-MESSAGES-250.csv', 'w')

    sorders = StockOrders()
    for g in gendata:
        action = dataset.to_string(g[0])

        # if action in ['A', 'F', 'E', 'C', 'X', 'D', 'U', 'P']:
        #     print(record.to_string())

        if action in ['F', 'A']:
            stock = dataset.to_string(g[7]).strip()

            if stock in sstocks:
                record = ITCHRecord(g)
                sorders.insert_order(stock, action, record.ORN)
                wfile.write('%s, %s\n'%(stock.strip(), record.to_string()))

        if action in ['E', 'C', 'X', 'D', 'U']:
            record = ITCHRecord(g)
            stock = sorders.query_id(record.ORN)
            if  stock is not None and stock in sstocks:
                wfile.write('%s, %s\n'%(stock.strip(), record.to_string()))
            if action == 'U':
                sorders.insert_order(stock, action, record.nORN)


        if i == 1000000:
            itime = ITCHtime(g[3])
            print(i,  g[3], itime.to_string())
            i = 0
            wfile.flush()
        i += 1
    now()

    cmp = Company()

    wfile.close()

