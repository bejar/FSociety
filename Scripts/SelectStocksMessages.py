"""
.. module:: Stocks

Stocks
*************

:Description: Stocks

    Selecciona los mensajes F/A/E/X/D/U/C que aparecen en un dia para las
    companyias en el fichero 'stockselected.csv' (250 companyias con mas operaciones
    de compra/venta)

:Authors: bejar
    

:Version: 

:Created on: 05/09/2016 12:04 

"""

import argparse
import os

from FSociety.ITCH import ITCHv5, ITCHRecord
from FSociety.Util import now
from FSociety.Data import Stock, StockOrders
from FSociety.Config import datapath, ITCH_days

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

    # for filename in [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]:
    for filename, dname in zip(lfiles, ITCH_days[year]):
        now()
        i = 0
        dataset = ITCHv5(datapath + filename)
        gendata = dataset.records()
        stockdic = {}
        print(filename)
        # dname = filename.split('.')[0]
        wfile = open(datapath + 'Results/' + dname + '-STOCK-MESSAGES-250.csv', 'w')
        sorders = StockOrders()
        for g in gendata:
            order = dataset.to_string(g[0])
            if order in ['F', 'A']:
                stock = dataset.to_string(g[7]).strip()
                if stock in sstocks.sstocks:
                    record = ITCHRecord(g)
                    sorders.insert_order(stock, order, record.ORN, record.timestamp)
                    wfile.write('#%s#, %s\n' % (stock.strip(), record.to_string()))

            if order in ['E', 'C', 'X', 'D', 'U']:
                record = ITCHRecord(g)
                stock = sorders.query_id(record.ORN)
                if stock is not None:
                    stock = stock[0]
                    if stock in sstocks.sstocks:
                        wfile.write('#%s#, %s\n' % (stock.strip(), record.to_string()))
                        if order == 'U':
                            sorders.insert_order(stock, order, record.nORN, updid=record.ORN, otime=record.timestamp,
                                                 price=record.price)
                        if order == 'D':
                            sorders.insert_order(stock, order, record.ORN)

            if order in ['P']:
                record = ITCHRecord(g)
                stock = record.stock
                if stock is not None and stock in sstocks.sstocks:
                    wfile.write('#%s#, %s\n' % (stock.strip(), record.to_string()))

            if i == 1000000:
                # itime = ITCHtime(g[3])
                # print(i,  g[3], itime.to_string())
                i = 0
                wfile.flush()
            i += 1
        now()
        wfile.close()
        os.system(' gzip ' + datapath + '/Results/' + dname + '-STOCK-MESSAGES-250.csv')
        for stock in sstocks.get_list_stocks():
            print(dname, stock)
            os.system(' zcat ' + datapath + '/Results/' + dname + '-STOCK-MESSAGES-250.csv.gz |grep \'#'
                      + stock + '#' + '\' > ' + datapath + '/Messages/' + dname + '-' + stock + '-MESSAGES.csv')
            os.system('  gzip ' + datapath + '/Messages/' + dname + '-' + stock + '-MESSAGES.csv')
