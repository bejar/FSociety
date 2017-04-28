"""
.. module:: Stocks

Stocks
*************

:Description: Stocks

    Genera una lista del numero de mensajes de venta/compra que aparecen en un dia para cada compañia

:Authors: bejar
    

:Version: 

:Created on: 05/09/2016 12:04 

"""


import argparse
from FSociety.Util import ITCH_days, datapath, Company, ITCHRecord, ITCHtime, now, ITCHv5

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default=None)

    args = parser.parse_args()
    year = args.year

    filename = ITCH_days[year][2] + '.NASDAQ_ITCH50.gz'
    now()
    i = 0

    dataset = ITCHv5(datapath + filename)

    gendata = dataset.records()

    stockdic = {}

    print(filename)
    for g in gendata:
        record = ITCHRecord(g)
        action = dataset.to_string(g[0])

        # if action in ['A', 'F', 'E', 'C', 'X', 'D', 'U', 'P']:
        #     print(record.to_string())


        if action in ['F', 'A']:
            stock = dataset.to_string(g[7])
            order = dataset.to_string(g[5])

            if not stock in stockdic:
                stockdic[stock] = {}
            if not order in stockdic[stock]:
                stockdic[stock][order] = 1
            else:
                stockdic[stock][order] += 1
        if i == 1000000:
            itime = ITCHtime(g[3])
            print(i, g[3], itime.to_string())

            i = 0
        i += 1
    now()

    cmp = Company()

    dname = filename.split('.')[0]
    wfile = open(datapath + '/Results/' + dname + '-STOCK-ACTIVITY.csv', 'w')
    for val in stockdic:
        cvalues = cmp.get_company(val.strip())
        sell = 0
        if 'S' in stockdic[val]:
            sell = stockdic[val]['S']
        buy = 0
        if 'B' in stockdic[val]:
            buy = stockdic[val]['B']
        if cvalues is not None:
            wfile.write('%s, %d, %d, %s, %s\n' % (val.strip(), buy, sell, cvalues[0], cvalues[1]))
        else:
            wfile.write('%s, %d, %d, None, None\n' % (val.strip(), buy, sell))
    wfile.close()
