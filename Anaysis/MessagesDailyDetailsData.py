"""
.. module:: MessagesDailyDetailsData

MessagesDailyDetailsData
*************

:Description: MessagesDailyDetailsData

    

:Authors: bejar
    

:Version: 

:Created on: 13/11/2017 9:34 

"""

import argparse

import gzip

import numpy as np


from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company
from FSociety.Config import datapath, ITCH_days
import pickle

__author__ = 'bejar'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='')

    args = parser.parse_args()
    year = str(args.year)
    sstocks = Stock()

    if year == '':
        year = '2017G'

    if 'G' in year:
        lfiles = ['/S' + day + '-v50.txt.gz' for day in ITCH_days[year]]
        datapath = datapath + '/GIS/'
    else:
        lfiles = [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]

    sstock = Stock(num=50)
    cpny = Company()

    for stock in sorted(sstock.get_list_stocks()):
        for day in ITCH_days[year]:
            print(day, stock)


            lexecutionsS = []
            lexecutionsB = []
            ltimeOS = []
            ltimeOB = []
            lpriceOS = []
            lpriceOB = []
            lsizeOB = []
            lsizeOS = []
            ldelete = []

            ltimeEB = []
            ltimeES = []
            lpriceES = []
            lpriceEB = []
            ltimeEP = []  # Ordenes ocultas
            lpriceEP = []
            lsizeEB = []
            lsizeES = []
            lsizeEP = []

            sorders = OrdersProcessor()

            i = 0
            norders = 0
            rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')

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
                    sorders.process_order(stock, order, ORN, otime=timestamp.itime, bos=data[5].strip(), price=price, size=int(data[6].strip()))
                    norders += 1
                    if 0.5 < price < 1000:
                        if data[5].strip() == 'B':
                            lpriceOB.append(price)
                            ltimeOB.append(timestamp.itime)
                            lsizeOB.append(int(data[6].strip()))
                        else:
                            lpriceOS.append(price)
                            ltimeOS.append(timestamp.itime)
                            lsizeOS.append(int(data[6].strip()))

                if order == 'U':
                    nORN =  data[4].strip()
                    sorders.process_order(stock, order, nORN, timestamp.itime, updid=ORN, price=float(data[6].strip()), size=int(data[5].strip()))

                # Computes the time between placing and order and canceling it
                if order == 'D':
                    trans = sorders.query_id(ORN).otime
                    ldelete.append(timestamp.itime - trans)
                    sorders.process_order(stock, order, ORN)

                # Computes the time between placing and order and its execution
                if order in ['E', 'C']:
                    trans = sorders.query_id(ORN).otime
                    if trans[2] == 'S':
                        lexecutionsS.append(timestamp.itime - trans)
                        ltimeES.append(timestamp.itime)
                        lpriceES.append(trans[3])
                        lsizeES.append(trans[4])
                    else:
                        lexecutionsB.append(timestamp.itime - trans)
                        ltimeEB.append(timestamp.itime)
                        lpriceEB.append(trans[3])
                        lsizeEB.append(trans[4])

                # Non-displayable orders
                if order in ['P']:
                    ltimeEP.append(timestamp.itime)
                    lpriceEP.append(float(data[7].strip()))
                    lsizeEP.append(int(data[6].strip()))

            print('Stock:', stock, 'Day:', day)
            print('N Buy orders:', len(ltimeOB))
            print('N Sell orders:', len(ltimeOS))
            print('N Order Executions Sell:', len(lexecutionsS))
            print('Mean time to execution:', nanoseconds_to_time(np.mean(lexecutionsS)))
            print('Max time to execution:', nanoseconds_to_time(np.max(lexecutionsS)))
            print('Min time to execution:', nanoseconds_to_time(np.min(lexecutionsS)))
            print('N Order Executions Buy:', len(lexecutionsB))
            print('Mean time to execution:', nanoseconds_to_time(np.mean(lexecutionsB)))
            print('Max time to execution:', nanoseconds_to_time(np.max(lexecutionsB)))
            print('Min time to execution:', nanoseconds_to_time(np.min(lexecutionsB)))
            print('N Hiden Executions:', len(ltimeEP))


            ddata = {}

            ddata['DeltaTimeExecBuy'] = lexecutionsB
            ddata['DeltaTimeExecSell'] = lexecutionsS
            ddata['TimeExecBuy'] = ltimeEB
            ddata['TimeExecSell'] = ltimeES
            ddata['PriceExecSell'] = lpriceES
            ddata['PriceExecBuy'] = lpriceEB
            ddata['SizeExecBuy'] = lsizeEB
            ddata['SizeExecSell'] = lsizeES

            ddata['TimeExecHidden'] = ltimeEP
            ddata['PriceExecHidden'] = lpriceEP
            ddata['SizeExecHidden'] = lsizeEP

            ddata['TimeOrderSell'] = ltimeOS
            ddata['TimeOrderBuy'] = ltimeOB
            ddata['PriceOrderSell'] = lpriceOS
            ddata['PriceOrderBuy'] = lpriceOB
            ddata['SizeOrderBuy'] = lsizeOB
            ddata['SizeOrderSell'] = lsizeOS

            ddata['DeltaTimeDelete'] = ldelete


            wfile = open(datapath + '/Results/' + day + '-' + stock + '-MessageAnalysis.pkl', 'wb')
            pickle.dump(ddata, wfile)
            wfile.close()
