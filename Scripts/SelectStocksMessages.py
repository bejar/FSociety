"""
.. module:: Stocks

Stocks
*************

:Description: Stocks

    Selecciona los mensajes F/A/E/X/D/U/C que aparecen en un dia para las 'nstock'
    companyias en el fichero 'stockmonthcsv') (companyias con mas operaciones
    de compra/venta)

:Authors: bejar
    

:Version: 

:Created on: 05/09/2016 12:04 

"""

import argparse
import os

from FSociety.ITCH import ITCHv5, ITCHRecord
from FSociety.Util import now
from FSociety.Data import Stock, OrdersProcessor
from FSociety.Config import datapath, ITCH_days

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='')
    parser.add_argument('--nstocks', help="Anyo del analisis", default=50)

    args = parser.parse_args()
    year = str(args.year)
    sstocks = Stock(num=args.nstocks)

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
        print(filename)
        wfile = open(datapath + 'Results/' + dname + '-STOCK-MESSAGES.csv', 'w')
        dorders = {}  # Dictionary to store the F/A/U orders to obtain the stock of U orders
        for g in gendata:
            order = dataset.to_string(g[0])

            if order in ['F', 'A']:
                stock = dataset.to_string(g[7]).strip()
                if stock in sstocks.sstocks:
                    record = ITCHRecord(g)
                    dorders[record.ORN] = stock
                    wfile.write('#%s#&%s\n' % (stock.strip(), record.to_string()))

            if order in ['E', 'C', 'X', 'D', 'U']:
                record = ITCHRecord(g)
                if order == 'U':  # U orders replace active orders
                    id = record.nORN
                    dorders[record.ORN] = stock
                else:
                    id = record.ORN
                if id in dorders:
                    stock = dorders[id]
                    wfile.write('#%s#&%s\n' % (stock.strip(), record.to_string()))

            if order in ['P']:
                record = ITCHRecord(g)
                stock = record.stock
                if stock is not None and stock in sstocks.sstocks:
                    wfile.write('#%s#&%s\n' % (stock.strip(), record.to_string()))

            if i == 1000000:
                i = 0
                wfile.flush()
            i += 1
        now()
        wfile.close()
        os.system(' gzip ' + datapath + '/Results/' + dname + '-STOCK-MESSAGES.csv')
        for stock in sstocks.get_list_stocks():
            print(dname, stock)
            os.system(' zcat ' + datapath + '/Results/' + dname + '-STOCK-MESSAGES.csv.gz |grep \'#'
                      + stock + '#' + '\' > ' + datapath + '/Messages/' + dname + '-' + stock + '-MESSAGES.csv')
            os.system('  gzip ' + datapath + '/Messages/' + dname + '-' + stock + '-MESSAGES.csv')
