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

from Util import  datapath, StockOrders, ITCH_days,  nanoseconds_to_time, Company

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.__version__ = '0.18'

__author__ = 'bejar'

if __name__ == '__main__':
    stock = 'AAL'
    day = ITCH_days[0]
    sorders = StockOrders()
    cpny = Company()
    rfile = open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv', 'r')

    lexecutionsS = []
    lexecutionsB = []
    ltimeOS = []
    ltimeOB = []
    lpriceOS = []
    lpriceOB = []
    ldelete = []

    ltimeEB = []
    ltimeES = []
    lpriceES = []
    lpriceEB = []

    i = 0
    norders = 0
    for mess in rfile:
        data = mess.split(',')
        timestamp = int(data[1].strip())
        order = data[2].strip()
        ORN = data[3].strip()
        if order in ['F', 'A']:
            if order == 'A':
                price = float(data[7].strip())
            else:
                price = float(data[8].strip())
            sorders.insert_order(stock, order, ORN, otime=timestamp, bos=data[5].strip(), price=price)
            norders += 1
            if 0.5 < price < 1000:
                if data[5].strip() == 'B':
                    lpriceOB.append(price)
                    ltimeOB.append(timestamp)
                else:
                    lpriceOS.append(price)
                    ltimeOS.append(timestamp)
        if order == 'U':
            nORN =  data[4].strip()
            sorders.insert_order(stock, order, nORN, timestamp, updid=ORN, price=data[6].strip())
        # Computes the time between placing and order and canceling it
        if order == 'D':
            trans = sorders.query_id(ORN)
            ldelete.append(timestamp - trans[1])
            sorders.insert_order(stock, order, ORN)
        # Computes the time between placing and order and its execution
        if order in ['E', 'C']:
            trans = sorders.query_id(ORN)
            if trans[2] == 'S':
                lexecutionsS.append(timestamp - trans[1])
                ltimeES.append(timestamp)
                lpriceES.append(trans[3])
            else:
                lexecutionsB.append(timestamp - trans[1])
                ltimeEB.append(timestamp)
                lpriceEB.append(trans[3])
        i += 1
        if i % 10000 == 0:
            print('.', end='', flush=True)

    print()
    print('Stock:', stock)
    if cpny.get_company(stock) is not None:
        print(cpny.get_company(stock))
    print('N Buy/Sell orders:', norders)
    if len(lexecutionsS) != 0:
        print('N Order Executions Sell:', len(lexecutionsS))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(lexecutionsS)))
        print('Max time to execution:', nanoseconds_to_time(np.max(lexecutionsS)))
        print('Min time to execution:', nanoseconds_to_time(np.min(lexecutionsS)))
        ax = sns.distplot(np.log10(lexecutionsS), kde=True, norm_hist=True)
        plt.title('Log plot of Sell execution time ' + day)
        plt.show()
        plt.close()
        price_std = np.std(lpriceOS)
        price_mean = np.mean(lpriceOS)
        apriceOS = np.array(lpriceOS)
        apriceOS = apriceOS[np.logical_and(apriceOS > (price_mean - (price_std)),
                                           apriceOS < (price_mean + (price_std)))]
        ax = sns.distplot(apriceOS,  kde=True, norm_hist=True)
        plt.title('Orders Sell price ' + day)
        plt.show()
        plt.close()

    if len(lexecutionsB) != 0:
        print('N Order Executions Buy:', len(lexecutionsB))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(lexecutionsB)))
        print('Max time to execution:', nanoseconds_to_time(np.max(lexecutionsB)))
        print('Min time to execution:', nanoseconds_to_time(np.min(lexecutionsB)))
        ax = sns.distplot(np.log10(lexecutionsB),  kde=True, norm_hist=True)
        plt.title('Log plot of Buy execution time ' + day)
        plt.show()
        plt.close()
        price_std = np.std(lpriceOB)
        price_mean = np.mean(lpriceOB)
        apriceOB = np.array(lpriceOB)
        apriceOB = apriceOB[np.logical_and(apriceOB > (price_mean - (price_std)),
                                           apriceOB < (price_mean + (price_std)))]
        ax = sns.distplot(apriceOB,  kde=True, norm_hist=True)
        plt.title('Orders Buy price ' + day)
        plt.show()
        plt.close()

    if len(ldelete) != 0:
        print('N Order deletions:', len(ldelete))
        print('Mean time to deletion:', nanoseconds_to_time(np.mean(ldelete)))
        print('Max time to deletion:', nanoseconds_to_time(np.max(ldelete)))
        print('Min time to deletion:', nanoseconds_to_time(np.min(ldelete)))
        ax = sns.distplot(np.log10(ldelete), kde=True, norm_hist=True)
        plt.title('Log plot of deletion time ' + day)
        plt.show()
        plt.close()

    if len(lexecutionsB) != 0 and len(lexecutionsS) != 0:
        ax = sns.distplot(np.log10(lexecutionsS),  kde=True, hist=False, color='r')
        ax = sns.distplot(np.log10(lexecutionsB),  kde=True, hist=False, color='g')
        ax = sns.distplot(np.log10(ldelete),  kde=True, hist=False, color='k')
        plt.title('Sell/Buy/Deletion time ' + day)
        plt.show()
        plt.close()
        ax = sns.distplot(apriceOS,  kde=True, hist=False, color='r')
        ax = sns.distplot(apriceOB,  kde=True, hist=False, color='g')
        plt.show()
        plt.close()

    plt.plot(ltimeOS, lpriceOS, color='r')
    plt.plot(ltimeOB, lpriceOB, color='g')
    plt.plot(ltimeES, lpriceES, 'bo')
    plt.plot(ltimeEB, lpriceEB, 'co')

    plt.title('Order Sell/Buy price evolution ' + day)
    plt.show()
    plt.close()

