"""
.. module:: MessageRuns

MessageRuns
*************

:Description: MessageRuns

    

:Authors: bejar
    

:Version: 

:Created on: 13/10/2016 13:21 

"""

__author__ = 'bejar'


import gzip

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from FSociety.Config import datapath, ITCH_days
from FSociety.Data import Company, StockOrders
from FSociety.ITCH import ITCHtime

__author__ = 'bejar'

if __name__ == '__main__':

    stock = 'YHOO'
    day = ITCH_days[1]
    sorders = StockOrders()
    cpny = Company()
    rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')

    lexecutionsS = []
    lexecutionsB = []
    ltimeOS = []
    ltimeOB = []
    lpriceOS = []
    lpriceOB = []
    lsizeOB = []
    lsizeOS = []

    ldelete = []
    ldeleteB = []
    ldeleteS = []


    ltimeEB = []
    ltimeES = []
    lpriceES = []
    lpriceEB = []
    ltimeEP = []   # Ordenes ocultas
    lpriceEP = []
    lsizeEB = []
    lsizeES = []
    lsizeEP = []

    ltimeDB = []
    ltimeDPS = []
    ltimeDS = []
    ltimeDPB = []
    lsizeDS = []
    lsizeDB = []

    i = 0
    norders = 0
    for mess in rfile:
        data = mess.split(',')
        timestamp = ITCHtime(int(data[1].strip()))
        order = data[2].strip()
        ORN = data[3].strip()
        if order in ['F', 'A']:
            if order == 'A':
                price = float(data[7].strip())
            else:
                price = float(data[8].strip())
            sorders.insert_order(stock, order, ORN, otime=timestamp, bos=data[5].strip(), price=price, size=int(data[6].strip()))
            norders += 1
            if 0.5 < price < 1000:
                if data[5].strip() == 'B':
                    lpriceOB.append(price)
                    ltimeOB.append(timestamp.itime)
                    lsizeOB.append(int(data[6].strip()))
                else:
                    lpriceOS.append(price)
                    ltimeOS.append(timestamp.itime)
                    lsizeOS.append(int(data[6].strip()))
        if order == 'U':
            nORN =  data[4].strip()
            sorders.insert_order(stock, order, nORN, timestamp, updid=ORN, price=float(data[6].strip()), size=int(data[5].strip()))
        # Computes the time between placing and order and canceling it
        if order == 'D':
            trans = sorders.query_id(ORN)
            ldelete.append(timestamp.itime - trans[1])
            sorders.insert_order(stock, order, ORN)
            price = trans[3]
            if 0.5 < price < 2000:
                if trans[2] == 'B':
                    ldeleteB.append(timestamp.itime - trans[1])
                    # ltimeDB.append(timestamp.itime)
                    ltimeDB.append(trans[1])
                    ltimeDPB.append(trans[3])
                    lsizeDB.append(trans[4])
                else:
                    ldeleteS.append(timestamp.itime - trans[1])
                    # ltimeDS.append(timestamp.itime)
                    ltimeDS.append(trans[1])
                    ltimeDPS.append(trans[3])
                    lsizeDS.append(trans[4])


        # Computes the time between placing and order and its execution
        if order in ['E', 'C']:
            trans = sorders.query_id(ORN)
            if trans[2] == 'S':
                lexecutionsS.append(timestamp.itime - trans[1])
                ltimeES.append(timestamp.itime)
                lpriceES.append(trans[3])
                lsizeES.append(trans[4])
            else:
                lexecutionsB.append(timestamp.itime - trans[1])
                ltimeEB.append(timestamp.itime)
                lpriceEB.append(trans[3])
                lsizeEB.append(trans[4])
        if order in ['P']:
            ltimeEP.append(timestamp.itime)
            lpriceEP.append(float(data[7].strip()))
            lsizeEP.append(int(data[6].strip()))

        i += 1
        if i % 10000 == 0:
            print('.')

    ldeleteBL = np.log10(ldeleteB)
    ldeleteSL = np.log10(ldeleteS)

    ltimeDB = np.array(ltimeDB)
    ltimeDPB = np.array(ltimeDPB)
    lsizeDB = np.array(lsizeDB)
    ltimeDS = np.array(ltimeDS)
    ltimeDPS = np.array(ltimeDPS)
    lsizeDS = np.array(lsizeDS)

    scale = '100s' #  'mcs' 'mls'

    dscale = {'mcs': (0,3),
              'mls': (3,6),
              'sec': (6,9),
              '10s': (9,10),
              '100s': (9,11),
              '1000s': (11, 12),
              '10000s': (13,15)
    }


    tscale = '10000s'

    tscalemin, tscalemax  = dscale[tscale]

    cond = ldeleteBL < tscalemax
    # plt.scatter(ltimeDB[cond], ltimeDPB[cond], color='r')
    # cond = np.logical_and(6 < ldeleteBL, ldeleteBL < 8)
    # plt.scatter(ltimeDB[cond], ltimeDPB[cond], color='m')
    # cond = np.logical_and(8 < ldeleteBL, ldeleteBL < 9)
    # plt.scatter(ltimeDB[cond], ltimeDPB[cond], color='y')
    #
    # cond = ldeleteBL > tscalemin
    # plt.scatter(ltimeDB[cond], ltimeDPB[cond], color='r')#, s=lsizeDB[cond])
    #
    # cond = ldeleteSL < 6
    # plt.scatter(ltimeDS[cond], ltimeDPS[cond], color='b')
    # cond = np.logical_and(6 < ldeleteSL, ldeleteSL < 8)
    # plt.scatter(ltimeDS[cond], ltimeDPS[cond], color='c')
    # cond = np.logical_and(8 < ldeleteSL, ldeleteSL < 9)
    # plt.scatter(ltimeDS[cond], ltimeDPS[cond], color='k')
    #
    # cond = ldeleteSL > tscalemin
    # plt.scatter(ltimeDS[cond], ltimeDPS[cond], color='b')#, s=lsizeDS[cond])

    cond = np.logical_and(tscalemin < ldeleteBL, ldeleteBL < tscalemax)
    plt.scatter(ltimeDB[cond], ltimeDPB[cond], color='g')
    cond = np.logical_and(tscalemin < ldeleteSL, ldeleteSL < tscalemax)
    plt.scatter(ltimeDS[cond], ltimeDPS[cond], color='r')

    plt.scatter(ltimeEB, lpriceEB, color='r', marker='+', s=lsizeEB)
    plt.scatter(ltimeES, lpriceES, color='g', marker='+', s=lsizeES)
    plt.scatter(ltimeEP, lpriceEP, color='k', marker='+', s=lsizeES)
    plt.plot(ltimeEB, lpriceEB, color='r')
    plt.plot(ltimeES, lpriceES, color='g')
    plt.plot(ltimeEP, lpriceEP, color='k')

    plt.title('Order Deletions timescale ' + tscale + ' D=' + day)
    plt.show()
    plt.close()

