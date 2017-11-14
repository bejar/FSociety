"""
.. module:: MessageAnalysis

MessageAnalysis
*************

:Description: MessageAnalysis

    Grafico de los mensajes de una compañia
      - Numero de ordenes
      - Numero de ordenes de compra y venta
      - Distribucion de delta de tiempos de ordenes de compra y venta y ejecuciones
      - Distribucion de precios de compra y venta
      - Distribucion de delta de tiempo de ordenes de compra y venta y borrados
      - Secuencia de precios y ejecuciones
      - Distribucion de los tamaños de las ordenes

:Authors: bejar
    

:Version: 

:Created on: 27/09/2016 10:29 

"""

import gzip

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from FSociety.Util import datapath, StockOrders, ITCH_days, nanoseconds_to_time, Company, ITCHtime, capped_prices

pd.__version__ = '0.18'



__author__ = 'bejar'

if __name__ == '__main__':
    stock = 'GOOGL'
    day = ITCH_days[0]
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


    ltimeEB = []
    ltimeES = []
    lpriceES = []
    lpriceEB = []
    ltimeEP = []   # Ordenes ocultas
    lpriceEP = []
    lsizeEB = []
    lsizeES = []
    lsizeEP = []

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
            sorders.process_order(stock, order, ORN, otime=timestamp, bos=data[5].strip(), price=price, size=int(data[6].strip()))
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
            sorders.process_order(stock, order, nORN, timestamp, updid=ORN, price=float(data[6].strip()), size=int(data[5].strip()))
        # Computes the time between placing and order and canceling it
        if order == 'D':
            trans = sorders.query_id(ORN)
            ldelete.append(timestamp.itime - trans[1])
            sorders.process_order(stock, order, ORN)
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
        ax = sns.distplot(capped_prices(lpriceOS),  kde=True, norm_hist=True)
        plt.title('Orders Sell price ' + day)
        plt.show()
        plt.close()

    if len(lexecutionsB) != 0:
        print('N Order Executions Buy:', len(lexecutionsB))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(lexecutionsB)))
        print('Max time to execution:', nanoseconds_to_time(np.max(lexecutionsB)))
        print('Min time to execution:', nanoseconds_to_time(np.min(lexecutionsB)))
        print('N Hiden Executions:', len(ltimeEP))
        ax = sns.distplot(np.log10(lexecutionsB),  kde=True, norm_hist=True)
        plt.title('Log plot of Buy execution time ' + day)
        plt.show()
        plt.close()
        ax = sns.distplot(capped_prices(lpriceOB),  kde=True, norm_hist=True)
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
        ax = sns.distplot(capped_prices(lpriceOS),  kde=True, hist=False, color='r')
        ax = sns.distplot(capped_prices(lpriceOB),  kde=True, hist=False, color='g')
        plt.title('Sell/Buy orders prices distribution ' + day)
        plt.show()
        plt.close()
        ax = sns.distplot(capped_prices(lsizeOS),  kde=True, hist=True, color='r')
        ax = sns.distplot(capped_prices(lsizeOB),  kde=True, hist=True, color='g')
        plt.title('Sell/Buy orders sizes distribution ' + day)
        plt.show()
        plt.close()
        ax = sns.distplot(capped_prices(lsizeES),  kde=True, hist=True, color='r')
        ax = sns.distplot(capped_prices(lsizeEB),  kde=True, hist=True, color='g')
        ax = sns.distplot(capped_prices(lsizeEP),  kde=True, hist=True, color='k')
        plt.title('Sell/Buy/Hidden execution sizes distribution ' + day)
        plt.show()
        plt.close()
        ax = sns.distplot(capped_prices(lpriceES),  kde=True, hist=False, color='r')
        ax = sns.distplot(capped_prices(lpriceEB),  kde=True, hist=False, color='g')
        ax = sns.distplot(capped_prices(lpriceEP),  kde=True, hist=False, color='k')
        plt.title('Sell/Buy/Hidden execution prices distribution ' + day)
        plt.show()
        plt.close()

    plt.plot(ltimeOS, lpriceOS, color='r')
    plt.plot(ltimeOB, lpriceOB, color='g')
    plt.scatter(ltimeES, lpriceES,  marker='o', color='y', s=lsizeES)
    plt.scatter(ltimeEB, lpriceEB,  marker='o', color='b', s=lsizeEB)
    plt.scatter(ltimeEP, lpriceEP, marker='o', color='k', s=lsizeEP)

    plt.title('Order Sell/Buy price evolution ' + day)
    plt.show()
    plt.close()

