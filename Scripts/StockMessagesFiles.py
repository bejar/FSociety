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

from Util import datapath, ITCH_files, Stock
import os

__author__ = 'bejar'


if __name__ == '__main__':


    sstocks = Stock()

    for filename in ['12302016.NASDAQ_ITCH50.gz']: #ITCH_files:
        dname = filename.split('.')[0]
        for stock in sstocks.get_list_stocks():
            print(dname, stock)
            os.system(' zcat ' + datapath + '/Results/' + dname +
                      '-STOCK-MESSAGES-250.csv.gz |grep \'#'+stock+'\' > ' +datapath + '/Messages/' + dname + '-' + stock +'-MESSAGES.csv' )
