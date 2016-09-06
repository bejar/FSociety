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
from Util import now
import pandas as pd
pd.__version__ = '0.18'
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from Constants import ITCH_files, datapath, NASDAQ_actions

__author__ = 'bejar'


if __name__ == '__main__':
    filename = ITCH_files[1]
    now()
    i= 0

    dataset = ITCHv5(datapath + filename)

    gendata = dataset.records()

    stockdic = {}

    print(filename)
    for g in gendata:
        action = dataset.to_string(g[0])

        if action in ['F', 'A']:
            stock = dataset.to_string(g[7])
            order = dataset.to_string(g[5])
            if not stock in stockdic:
                stockdic[stock] = {}
            if not order in stockdic[stock]:
                stockdic[stock][order] = 1
            else:
                 stockdic[stock][order] += 1
        if i > 1000000:
            itime = ITCHtime(g[3])
            print(i,  g[3], itime.to_string())
            #summarize_stock_action_agent(stockdic)
            # for v in actionsdic:
            #     print(v, actionsdic[v])
            #     print('##################################')
            i = 0
        i += 1
    now()

    for val in stockdic:
        print(val, stockdic[val])

