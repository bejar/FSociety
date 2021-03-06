"""
.. module:: Stocks

Stocks
*************

:Description: Stocks

    Selecciona los mensajes F/A/E/X/D/U/C que aparecen en un dia para las 'nstock'
    companyias en el fichero 'stockmonth.csv') (companyias con mas operaciones
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

def process_messages(filename, dname):
        now()
        i = 0
        dataset = ITCHv5(datapath + filename)
        gendata = dataset.records()
        print(filename)
        wfile = open(f'{datapath}/Results/{dname}-STOCK-MESSAGES.csv', 'w')
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
                        if order == 'D':
                            del dorders[record.ORN]
                        wfile.write(f'#{stock.strip()}#&{record.to_string()}\n')

            # Replace orders have the old id order in oORN
            if order in ['U']:
                record = ITCHRecord(g)
                if record.oORN in dorders:
                    stock = dorders[record.oORN]
                    dorders[record.ORN] = dorders[record.oORN]
                    del dorders[record.oORN]
                    wfile.write(f'#{stock.strip()}#&{record.to_string()}\n')

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
        now()
        wfile.close()
        os.system(f' gzip {datapath}/Results/{dname}-STOCK-MESSAGES.csv')
        for stock in sstocks.get_list_stocks():
            print(dname, stock)
            os.system(' zcat ' + datapath + '/Results/' + dname + '-STOCK-MESSAGES.csv.gz |grep \'#'
                      + stock + '#' + '\' > ' + datapath + '/Messages/' + dname + '-' + stock + '-MESSAGES.csv')
            os.system('  gzip ' + datapath + '/Messages/' + dname + '-' + stock + '-MESSAGES.csv')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Year of the analysis", default='2017G')
    parser.add_argument('--nstocks', help="Number of stocks to analyze", type=int, default=50)
    parser.add_argument('--init', help="Initial Day", type=int, default=0)
    parser.add_argument('--day', help="Specific Day", type=int, default=None)

    args = parser.parse_args()
    year = str(args.year)
    sstocks = Stock(num=args.nstocks)
    print(len(sstocks.sstocks))

    if 'G' in year:
        lfiles = [f'/S{day}-v50.txt.gz' for day in ITCH_days[year]]
        datapath = datapath + '/GIS/'
    else:
        lfiles = [f'{day}.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]

    if args.day is None:
        # for filename in [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]:
        for filename, dname in zip(lfiles[args.init:], ITCH_days[year][args.init:]):
            process_messages(filename,dname)
    else:
        filename = lfiles[args.day]
        dname = ITCH_days[year][args.day]
        process_messages(filename,dname)



