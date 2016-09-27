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

    for filename in ITCH_files:
        now()
        i= 0
        dataset = ITCHv5(datapath + filename)
        gendata = dataset.records()
        stockdic = {}
        print(filename)
        dname = filename.split('.')[0]
        wfile = open(datapath + '/Results/' + dname + '-STOCK-MESSAGES-250.csv', 'w')
        sorders = StockOrders()
        for g in gendata:
            action = dataset.to_string(g[0])
            if action in ['F', 'A']:
                stock = dataset.to_string(g[7]).strip()
                if stock in sstocks:
                    record = ITCHRecord(g)
                    sorders.insert_order(stock, action, record.ORN)
                    wfile.write('#%s, %s\n'%(stock.strip(), record.to_string()))

            if action in ['E', 'C', 'X', 'D', 'U']:
                record = ITCHRecord(g)
                stock = sorders.query_id(record.ORN)
                if  stock is not None and stock in sstocks:
                    wfile.write('#%s, %s\n'%(stock.strip(), record.to_string()))
                if action == 'U':
                    sorders.insert_order(stock, action, record.nORN)
                if action == 'D':
                    sorders.insert_order(stock, action, record.ORN)

            if i == 1000000:
                #itime = ITCHtime(g[3])
                #print(i,  g[3], itime.to_string())
                i = 0
                wfile.flush()
            i += 1
        now()

        wfile.close()

