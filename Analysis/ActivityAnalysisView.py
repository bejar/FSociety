"""
.. module:: OrdersActivityCountsView

OrdersActivityCountsView
*************

:Description: OrdersActivityCountsView

    

:Authors: bejar
    

:Version: 

:Created on: 11/03/2019 13:42 

"""

import argparse

from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter
from FSociety.Config import datapath, ITCH_days
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from FSociety.Util import nanoseconds_to_time, capped_prices
import pickle

__author__ = 'bejar'

def plot_tscale():
    plt.plot([3,3],[0,0.1], 'r')
    plt.plot([6,6],[0,0.1], 'r')
    plt.plot([9,9],[0,0.1], 'r')
    plt.plot([10,10],[0,0.05], 'g')
    plt.plot([11,11],[0,0.05], 'g')

def plot_statistics(statistics):
    """
    Some plot of the results
    :param statistics:
    :return:
    """
    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(np.log10(statistics['sell']['executiondeltatime']), kde=True, norm_hist=True)
    plot_tscale()
    plt.title(f'Log plot of Sell execution delta time {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(capped_prices(statistics['sell']['executionprice']), kde=True, norm_hist=True)
    plt.title(f'Orders Sell price {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(np.log10(statistics['buy']['executiondeltatime']), kde=True, norm_hist=True)
    plot_tscale()
    plt.title(f'Log plot of Buy execution time {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(capped_prices(statistics['buy']['executionprice']), kde=True, norm_hist=True)
    plt.title(f'Orders Buy price {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(np.log10(statistics['buy']['deletedeltatime']), kde=True, norm_hist=True, label='Buy')
    ax = sns.distplot(np.log10(statistics['sell']['deletedeltatime']), kde=True, norm_hist=True, label='Sell')
    plot_tscale()
    plt.legend()
    plt.title(f'Log plot of deletion time (Buy/Sell) {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(np.log10(statistics['sell']['executiondeltatime']), kde=True, hist=False, color='r',
                      label='Exec Buy')
    ax = sns.distplot(np.log10(statistics['buy']['executiondeltatime']), kde=True, hist=False, color='g',
                      label='Exec Sell')
    ax = sns.distplot(np.log10(statistics['buy']['deletedeltatime']), kde=True, hist=False, color='b',
                      label='Del Buy')
    ax = sns.distplot(np.log10(statistics['sell']['deletedeltatime']), kde=True, hist=False, color='k',
                      label='Del Sell')
    plt.legend()
    plot_tscale()
    plt.title(f'Sell/Buy/Deletion time {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(capped_prices(statistics['sell']['orderprice']), kde=True, hist=False, color='r',
                      label='Sell')
    ax = sns.distplot(capped_prices(statistics['buy']['orderprice']), kde=True, hist=False, color='g', label='Buy')
    plt.legend()
    plt.title(f'Sell/Buy orders prices distribution {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(capped_prices(statistics['sell']['ordersize']), kde=False, hist=True, color='r', label='Sell')
    ax = sns.distplot(capped_prices(statistics['buy']['ordersize']), kde=False, hist=True, color='g', label='Buy')
    plt.title(f'Sell/Buy orders sizes distribution {itchday} {args.stock}', fontsize=20)
    plt.legend()
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(capped_prices(statistics['sell']['executionprice']), kde=True, hist=False, color='r',
                      label='Sell')
    ax = sns.distplot(capped_prices(statistics['buy']['executionprice']), kde=True, hist=False, color='g',
                      label='Buy')
    plt.legend()
    plt.title(f'Sell/Buy execution prices distribution {itchday} {args.stock}', fontsize=20)
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = sns.distplot(capped_prices(statistics['sell']['executionsize']), kde=False, hist=True, color='r',
                      label='Sell')
    ax = sns.distplot(capped_prices(statistics['buy']['executionsize']), kde=False, hist=True, color='g',
                      label='Buy')
    plt.title(f'Sell/Buy execution sizes distribution {itchday} {args.stock}', fontsize=20)
    plt.legend()
    plt.show()

    fig = plt.figure(figsize=(14, 8))
    plt.plot(statistics['sell']['ordertime'], statistics['sell']['orderprice'], color='r')
    plt.plot(statistics['buy']['ordertime'], statistics['buy']['orderprice'], color='g')
    plt.scatter(statistics['sell']['executiontime'], statistics['sell']['executionprice'], marker='o', color='y',
                s=statistics['sell']['executionsize'])
    plt.scatter(statistics['buy']['executiontime'], statistics['buy']['executionprice'], marker='o', color='b',
                s=statistics['buy']['executionsize'])

    plt.title(f'Order Sell/Buy price evolution ', fontsize=20)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')
    parser.add_argument('--day', help="dia del anyo", type=int, default=0)
    parser.add_argument('--stock', help="Stock del analisis", default='GOOGL')
    parser.add_argument('--kde', help="Show Kernel Density Estimation", action='store_true', default=False)
    parser.add_argument('--bins', help="Number of histogram bins", type=int, default=10)

    args = parser.parse_args()
    itchday = ITCH_days[args.year][args.day]
    if 'G' in args.year:
        # lfiles = [f'/S{day}-v50.txt.gz' for day in ITCH_days[year]]
        # datapath = datapath + '/GIS/'
        analysispath = datapath + '/GIS/Analysis'
    else:
        # lfiles = [f'{day}.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]
        analysispath = datapath + '/Analysis'


    rfile = open(f'{analysispath}/{ITCH_days[args.year][args.day]}-{args.stock}-ActivityStatistics.pkl', 'rb')
    statistics = pickle.load(rfile)
    rfile.close()
    plot_statistics(statistics)