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

__author__ = 'bejar'


if __name__ == '__main__':
    filename = ITCH_files[2]
    now()
    i= 0

    dataset = ITCHv5(datapath + filename)

    gendata = dataset.records()

    stockdic = {}

    print(filename)
    for g in gendata:
        record = ITCHRecord(g)
        action = dataset.to_string(g[0])

        if action in ['A', 'F', 'E', 'C', 'X', 'D', 'U', 'P']:
            print(record.to_string())


        if action in ['F', 'A']:
            stock = dataset.to_string(g[7])
            order = dataset.to_string(g[5])

            if not stock in stockdic:
                stockdic[stock] = {}
            if not order in stockdic[stock]:
                stockdic[stock][order] = 1
            else:
                 stockdic[stock][order] += 1
        if i == 1000000:
            itime = ITCHtime(g[3])
            print(i,  g[3], itime.to_string())
            #summarize_stock_action_agent(stockdic)
            # for v in actionsdic:
            #     print(v, actionsdic[v])
            #     print('##################################')
            i = 0
        i += 1
    now()

    cmp = Company()

    dname = filename.split('.')[0]
    wfile = open(datapath + '/Results/' + dname + '-STOCK-ACTIVITY.csv', 'w')
    for val in stockdic:
        cvalues = cmp.get_company(val.strip())
        sell = 0
        if 'S' in stockdic[val]:
            sell =  stockdic[val]['S']
        buy = 0
        if 'B' in stockdic[val]:
            buy = stockdic[val]['B']
        if cvalues is not None:
           wfile.write('%s, %d, %d, %s, %s\n' % (val.strip(), buy, sell,  cvalues[0],  cvalues[1]))
        else:
            wfile.write('%s, %d, %d, None, None\n' % (val.strip(), buy, sell))
    wfile.close()

