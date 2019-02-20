"""
.. module:: MessagesAnalysisData

MessagesAnalysisData
*************

:Description: MessagesAnalysisData

    Computes diverse statistics from the messages [Buy, Sell, Delete, Execution] of a day for a set of stocks



:Authors: bejar
    

:Version: 

:Created on: 29/09/2016 15:47 

"""

import argparse

import gzip

import numpy as np


from FSociety.ITCH import ITCHtime, ITCHMessages
from FSociety.Util import now
from FSociety.Data import Stock, OrdersProcessor, Company
from FSociety.Config import datapath, ITCH_days


__author__ = 'bejar'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')

    args = parser.parse_args()
    year = str(args.year)
    sstocks = Stock()

    # if year == '':
    #     year = '2017G'

    if 'G' in year:
        lfiles = ['/S' + day + '-v50.txt.gz' for day in ITCH_days[year]]
        datapath = datapath + '/GIS/'
    else:
        lfiles = [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]

    sstock = Stock(num=50)
    cpny = Company()
    wfile = open(datapath + '/Results/MessagesStats.csv', 'w')
    wfile.write('Day,Stock,N Buy/Sell orders,N Order Executions Sell,Mean time to execution,Max time to execution,Min time to execution,'
                'N Order Executions Buy,Mean time to execution,Max time to execution,Min time to execution,'
                'N Order deletions,Mean time to deletion,Max time to deletion,Min time to deletion\n')
    for stock in sorted(sstock.get_list_stocks()):
        for id, day in enumerate(ITCH_days[year]):
            print(day, stock)
            sorders = OrdersProcessor()

            rfile = ITCHMessages(year, day, stock)
            rfile.open()
            rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')

            lexecutionsS = []
            lexecutionsB = []
            ldelete = []

            i = 0
            norders = 0
            for order in rfile.get_order():
                sorders.insert_order(order)

                if order.type == 'D':
                    trans = sorders.query_id(order.id)
                    ldelete.append(order.otime - trans.otime)
                # Computes the time between placing and order and its execution
                if order in ['E', 'C']:
                    trans = sorders.query_id(order.id)
                    if trans.buy_sell == 'S':
                        lexecutionsS.append(order.otime - trans.otime)
                    else:
                        lexecutionsB.append(order.otime - trans.otime)
                i += 1
                if i % 10000 == 0:
                    print('.', end='')
                    wfile.flush()

            if len(lexecutionsB) != 0 and len(lexecutionsS) != 0:
                wfile.write(day + ',' + stock + ',' + str(norders) + ',')
                wfile.write(str(len(lexecutionsS)) + ',' + str(np.mean(lexecutionsS)) + ',' + str(np.max(lexecutionsS)) + ','+ str(np.min(lexecutionsS)) + ',')
                wfile.write(str(len(lexecutionsB)) + ',' + str(np.mean(lexecutionsB)) + ',' + str(np.max(lexecutionsB)) + ','+ str(np.min(lexecutionsB)) + ',')
                wfile.write(str(len(ldelete)) + ',' + str(np.mean(ldelete)) + ',' + str(np.max(ldelete)) + ','+ str(np.min(ldelete)) + '\n')

            print()
            rfile.close()
    wfile.close()