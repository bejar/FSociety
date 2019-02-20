"""
.. module:: MessagesDailyDetailsData

MessagesDailyDetailsData
*************

:Description: MessagesDailyDetailsData

    Computes statistics for buy/sell orders and buy/sell executions for a day
    and saves the raw data in a pkl file

:Authors: bejar
    

:Version: 

:Created on: 13/11/2017 9:34 

"""

import argparse

import gzip

import numpy as np


from FSociety.ITCH import ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company
from FSociety.Config import datapath, ITCH_days
import pickle

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='')
    parser.add_argument('--day', help="dia del anyo", default='')

    args = parser.parse_args()
    year = str(args.year)

    if year == '':
        year = '2017G'

    if args.day == '':
        day = 0
    else:
        day = int(args.day)


    if 'G' in year:
        datapath = datapath + '/GIS/'

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--year', help="Anyo del analisis", default='')
    #
    # args = parser.parse_args()
    # year = str(args.year)
    # sstocks = Stock()
    #
    # if year == '':
    #     year = '2017G'
    #
    # if 'G' in year:
    #     lfiles = ['/S' + day + '-v50.txt.gz' for day in ITCH_days[year]]
    #     datapath = datapath + '/GIS/'
    # else:
    #     lfiles = [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]

    sstock = Stock(num=50)
    cpny = Company()

    for stock in ['YHOO']: #sorted(sstock.get_list_stocks()):
        # for day in enumerate(ITCH_days[year]):

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
            rfile = gzip.open(datapath + 'Messages/' + ITCH_days[year][day] + '-' + stock + '-MESSAGES.csv.gz', 'rt')

            rfile = ITCHMessages(year, day, stock)
            rfile.open()

            sorders = OrdersProcessor()

            # for mess in rfile:
            for order in rfile.get_order():
                # data = mess.split(',')
                # timestamp = ITCHtime(int(data[1].strip()))
                # order = data[2].strip()
                # ORN = data[3].strip()
                # print(order.to_string())
                sorders.insert_order(order)

                if order.type in ['F', 'A', 'U']:
                    # if order == 'A':
                    #     price = float(data[7].strip())
                    # else:
                    #     price = float(data[8].strip())
                    # sorders.process_order(stock, order, ORN, otime=timestamp.itime, bos=data[5].strip(), price=price, size=int(data[6].strip()))
                    norders += 1
                    if 0.5 < order.price < 1000:
                        if order.buy_sell == 'B':
                            lpriceOB.append(order.price)
                            ltimeOB.append(order.otime)
                            lsizeOB.append(order.size)
                        else:
                            lpriceOS.append(order.price)
                            ltimeOS.append(order.otime)
                            lsizeOS.append(order.size)

                # if order == 'U':
                #     nORN =  data[4].strip()
                #     sorders.process_order(stock, order, nORN, timestamp.itime, updid=ORN, price=float(data[6].strip()), size=int(data[5].strip()))

                # Computes the time between placing and order and canceling it
                if order.type == 'D':
                    trans = sorders.query_id(order.id)
                    if trans is not None:
                        ldelete.append(order.otime - trans.otime)
                    else:
                        print('MISSING DELETED' + order.id)
                    # sorders.process_order(stock, order, ORN)

                # Computes the time between placing and order and its execution
                if order.type in ['E', 'C']:
                    trans = sorders.query_id(order.id)
                    if trans.buy_sell == 'S':
                        lexecutionsS.append(order.otime - trans.otime)
                        ltimeES.append(order.otime)
                        lpriceES.append(trans.price)
                        lsizeES.append(trans.size)
                    else:
                        lexecutionsB.append(order.otime - trans.otime)
                        ltimeEB.append(order.otime)
                        lpriceEB.append(trans.price)
                        lsizeEB.append(trans.size)

                # Non-displayable orders
                if order.type in ['P']:
                    ltimeEP.append(order.otime)
                    lpriceEP.append(order.price)
                    lsizeEP.append(order.size)

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

            wfile = open(datapath + '/Results/' + ITCH_days[year][day] + '-' + stock + '-MessageAnalysis.pkl', 'wb')
            pickle.dump(ddata, wfile)
            wfile.close()
