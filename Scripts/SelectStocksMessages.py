"""
.. module:: Stocks

Stocks
*************

:Description: Stocks

    Selecciona los mensajes F/A/E/X/D/U/C que aparecen en un dia para las
    compañias en el fichero 'stockselected.csv' (250 compañias con mas operaciones
    de compra/venta)

:Authors: bejar
    

:Version: 

:Created on: 05/09/2016 12:04 

"""



import pandas as pd

from Util import ITCHv5, ITCHRecord, now, ITCH_files, datapath, StockOrders, ITCH_days

pd.__version__ = '0.18'


__author__ = 'bejar'


if __name__ == '__main__':

    file = '../Data/stockselected.csv'
    rfile = open(file, 'r')
    sstocks = set()
    for stock in rfile:
        sstocks.add(stock.strip())
    rfile.close()

    for filename in ['07292016.NASDAQ_ITCH50.gz', '08302016.NASDAQ_ITCH50.gz']: #ITCH_files:
        now()
        i = 0
        dataset = ITCHv5(datapath + filename)
        gendata = dataset.records()
        stockdic = {}
        print(filename)
        dname = filename.split('.')[0]
        wfile = open(datapath + '/Results/' + dname + '-STOCK-MESSAGES-250.csv', 'w')
        sorders = StockOrders()
        for g in gendata:
            order = dataset.to_string(g[0])
            if order in ['F', 'A']:
                stock = dataset.to_string(g[7]).strip()
                if stock in sstocks:
                    record = ITCHRecord(g)
                    sorders.insert_order(stock, order, record.ORN, record.timestamp)
                    wfile.write('#%s, %s\n'%(stock.strip(), record.to_string()))

            if order in ['E', 'C', 'X', 'D', 'U']:
                record = ITCHRecord(g)
                stock = sorders.query_id(record.ORN)
                if stock is not None:
                    stock = stock[0]
                    if stock in sstocks:
                        wfile.write('#%s, %s\n'%(stock.strip(), record.to_string()))
                        if order == 'U':
                            sorders.insert_order(stock, order, record.nORN, updid=record.ORN, otime=record.timestamp, price=record.price)
                        if order == 'D':
                            sorders.insert_order(stock, order, record.ORN)

            if order in ['P']:
                record = ITCHRecord(g)
                stock = record.stock
                if stock is not None and stock in sstocks:
                    wfile.write('#%s, %s\n'%(stock.strip(), record.to_string()))


            if i == 1000000:
                #itime = ITCHtime(g[3])
                #print(i,  g[3], itime.to_string())
                i = 0
                wfile.flush()
            i += 1
        now()

        wfile.close()

