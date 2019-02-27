"""
.. module:: TestFile

TestFile
*************

:Description: TestFile

    

:Authors: bejar
    

:Version: 

:Created on: 27/02/2019 10:41 

"""


import argparse
import os

from FSociety.ITCH import ITCHv5, ITCHRecord
from FSociety.Util import now
from FSociety.Data import Stock, OrdersProcessor
from FSociety.Config import datapath, ITCH_days

__author__ = 'bejar'

if __name__ == '__main__':

    year = '2017G'
    day = ITCH_days[year][0]
    #stock = 'GOOGL'
    sstocks = Stock(num=50)
    filename = f'/S{day}-v50.txt.gz'

    dataset = ITCHv5(datapath + '/GIS/'+ filename)
    gendata = dataset.records()
    print(filename)
    i = 0
    wfile = open(f'{datapath}/Results/{day}-STOCK-MESSAGES-zzz.csv', 'w')
    dorders = {}  # Dictionary to store the F/A/U orders to obtain the stock of U orders
    record = None
    for g in gendata:
        order = dataset.to_string(g[0])
        if order in ['F', 'A']:
            stock = dataset.to_string(g[7]).strip()
            if stock in sstocks.sstocks:
                record = ITCHRecord(g)
                dorders[record.ORN] = stock
                wfile.write(f'#{stock.strip()}#&{record.to_string()}\n')

        if order in ['E', 'C', 'X', 'D']:
            record = ITCHRecord(g)
            if record.ORN in dorders:
                stock = dorders[record.ORN]
                if stock in sstocks.sstocks:
                    if order== 'D':
                        del dorders[record.ORN]
                    wfile.write(f'#{stock.strip()}#&{record.to_string()}\n')

        if order in ['U']:
            record = ITCHRecord(g)
            if record.oORN in dorders:
                stock = dorders[record.oORN]
                if order == 'U':  # U orders replace active orders
                    dorders[record.ORN] = dorders[record.oORN]
                    del dorders[record.oORN]
                wfile.write(f'#{stock.strip()}#&{record.to_string()}\n')
                print(f'#{stock.strip()}#&{record.to_string()}')

        if order in ['P']:
            record = ITCHRecord(g)
            stock = record.stock
            if stock is not None and stock in sstocks.sstocks:
                wfile.write(f'#{stock.strip()}#&{record.to_string()}\n')

        if i == 1000000:
            i = 0
            if record is not None:
                print(record.timestamp.to_string(), flush=True)
            wfile.flush()
        i += 1
    wfile.close()
