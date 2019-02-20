"""
.. module:: StockMessagesFiles

StockMessagesFiles
*************

:Description: StockMessagesFiles

    Genera los ficheros separados con los mensajes de los stocks seleccionados

:Authors: bejar
    

:Version: 

:Created on: 27/09/2016 14:40 

"""

import os
import argparse
from FSociety.Config import datapath, ITCH_days
from FSociety.Data import Stock

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default="")

    args = parser.parse_args()
    year = str(args.year)
    if year == '':
        year = '2015'

    sstocks = Stock()

    # for filename in [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]:
    for filename in ['S021317-v50.txt.gz']:
        dname = filename.split('.')[0]
        for stock in sstocks.get_list_stocks():
            print(dname, stock)
            os.system(' zcat ' + datapath + '/GIS/Results/' + dname + '-STOCK-MESSAGES-250.csv.gz |grep \'#'
                      + stock + '#' + '\' > ' + datapath + '/GIS/Messages/' + dname + '-' + stock + '-MESSAGES.csv')
