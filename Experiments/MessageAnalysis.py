"""
.. module:: MessageAnalysis

MessageAnalysis
*************

:Description: MessageAnalysis

    Analisis de los mensajes de una compañia

:Authors: bejar
    

:Version: 

:Created on: 27/09/2016 10:29 

"""


import pandas as pd

from Util import ITCHv5, ITCHRecord, now, ITCH_files, datapath, StockOrders, ITCH_days, ITCHtime

pd.__version__ = '0.18'



__author__ = 'bejar'


if __name__ == '__main__':
    stock = 'GOOG'
    day = ITCH_days[2]

    rfile = open(datapath + day + '-' + stock + '-MESSAGES.csv', 'r')
    for mess in rfile:
        data = mess.split(',')



