"""
.. module:: StockMessagesFiles

StockMessagesFiles
*************

:Description: StockMessagesFiles

    Genera los ficheros con los mensajes de los stocks seleccionados

:Authors: bejar
    

:Version: 

:Created on: 27/09/2016 14:40 

"""

from Util import datapath, ITCH_files
import os

__author__ = 'bejar'


if __name__ == '__main__':

    file = '../Data/stockselected.csv'
    rfile = open(file, 'r')
    sstocks = set()
    for stock in rfile:
        sstocks.add(stock.strip())
    rfile.close()
    for filename in ITCH_files:
        dname = filename.split('.')[0]
        for stock in sstocks:
            print(dname, stock)
            os.system(' zcat ' + datapath + '/Results/' + dname +
                      '-STOCK-MESSAGES-250.csv.gz |grep \'#'+stock+'\' > ' +datapath + dname + '-' + stock +'-MESSAGES.csv' )
