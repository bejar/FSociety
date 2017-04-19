"""
.. module:: MessagesAnalysisData

MessagesAnalysisData
*************

:Description: MessagesAnalysisData

    

:Authors: bejar
    

:Version: 

:Created on: 29/09/2016 15:47 

"""

from Util import  datapath, StockOrders, ITCH_days,  nanoseconds_to_time, Company, Stock, ITCHtime

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import gzip

pd.__version__ = '0.18'

__author__ = 'bejar'

if __name__ == '__main__':

    sstock = Stock()
    cpny = Company()
    wfile = open(datapath + '/Results/MessagesStats.csv', 'w')
    wfile.write('Day,Stock,N Buy/Sell orders,N Order Executions Sell,Mean time to execution,Max time to execution,Min time to execution,'
                'N Order Executions Buy,Mean time to execution,Max time to execution,Min time to execution,'
                'N Order deletions,Mean time to deletion,Max time to deletion,Min time to deletion\n')
    for stock in sorted(sstock.get_list_stocks()):
        for fday in range(len(ITCH_days)):
            day = ITCH_days[fday]
            print(day, stock, end='', flush=True)
            sorders = StockOrders()

            rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')

            lexecutionsS = []
            lexecutionsB = []
            ldelete = []


            i = 0
            norders = 0
            for mess in rfile:
                data = mess.split(',')
                timestamp = ITCHtime(int(data[1].strip()))
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
                    ldelete.append(timestamp.itime - trans[1])
                    sorders.insert_order(stock, order, ORN)
                # Computes the time between placing and order and its execution
                if order in ['E', 'C']:
                    trans = sorders.query_id(ORN)
                    if trans[2] == 'S':
                        lexecutionsS.append(timestamp.itime - trans[1])
                    else:
                        lexecutionsB.append(timestamp.itime - trans[1])
                i += 1
                if i % 10000 == 0:
                    print('.', end='', flush=True)
                    wfile.flush()

            if len(lexecutionsB) != 0 and len(lexecutionsS) != 0:
                wfile.write(day + ',' + stock + ',' + str(norders) + ',')
                wfile.write(str(len(lexecutionsS)) + ',' + str(np.mean(lexecutionsS)) + ',' + str(np.max(lexecutionsS)) + ','+ str(np.min(lexecutionsS)) + ',')
                wfile.write(str(len(lexecutionsB)) + ',' + str(np.mean(lexecutionsB)) + ',' + str(np.max(lexecutionsB)) + ','+ str(np.min(lexecutionsB)) + ',')
                wfile.write(str(len(ldelete)) + ',' + str(np.mean(ldelete)) + ',' + str(np.max(ldelete)) + ','+ str(np.min(ldelete)) + '\n')

            print()
            rfile.close()
    wfile.close()