"""
.. module:: OrdersActivityCounts

OrdersActivityCounts
*************

:Description: OrdersActivityCounts

    

:Authors: bejar
    

:Version: 

:Created on: 11/03/2019 8:56 

"""
import argparse
from FSociety.Config import datapath, ITCH_days
from FSociety.Util import nanoseconds_to_time, capped_prices
from FSociety.ITCH import ITCHtime, ITCHMessages
from FSociety.Data import Stock, OrdersProcessor

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle

__author__ = 'bejar'


def plot_tscale():
    plt.plot([3,3],[0,0.1], 'r')
    plt.plot([6,6],[0,0.1], 'r')
    plt.plot([9,9],[0,0.1], 'r')
    plt.plot([10,10],[0,0.05], 'g')
    plt.plot([11,11],[0,0.05], 'g')

def order_statistics(year, day, stock):
    """
    Computes statistics for the orders of a stock

    :param year:
    :param day:
    :param stock:
    :return:
    """
    statistics = {'buy':
                      {'ordersize':[],
                       'ordertime':[],
                       'orderprice':[],
                       'executionsize':[],
                       'executionprice':[],
                       'executiondeltatime':[],
                       'executiontime':[],
                       'deletedeltatime':[]
                       },
                  'sell':
                      {'ordersize':[],
                       'ordertime':[],
                       'orderprice':[],
                       'executionsize':[],
                       'executionprice':[],
                       'executiontime':[],
                       'executiondeltatime':[],
                       'deletedeltatime':[]
                       },

                  }


    i = 0
    norders = 0

    rfile = ITCHMessages(year, day, stock)
    sorders = OrdersProcessor(history=True)
    rfile.open()


    for order in rfile.get_order():
        sorders.insert_order(order)

        if order.type in ['F', 'A', 'U']:
            norders += 1
            if 0.5 < order.price < 1000:
                if order.buy_sell == 'S':
                    statistics['sell']['ordersize'].append(order.size)
                    statistics['sell']['ordertime'].append(order.otime)
                    statistics['sell']['orderprice'].append(order.price)
                else:
                    statistics['buy']['ordersize'].append(order.size)
                    statistics['buy']['ordertime'].append(order.otime)
                    statistics['buy']['orderprice'].append(order.price)

        # If is a cancel/replace order consider also a deletion
        if order.type in ['U']:
            trans = sorders.query_id(order.oid)
            if order.buy_sell == 'S':
                statistics['sell']['deletedeltatime'].append(order.otime - trans.otime)
            else:
                statistics['buy']['deletedeltatime'].append(order.otime - trans.otime)

        # Computes the time between placing and order and canceling it
        if order.type == 'D':
            trans = sorders.query_id(order.id)
            if trans is not None:
                if trans.buy_sell == 'S':
                    statistics['sell']['deletedeltatime'].append(order.otime - trans.otime)
                else:
                    statistics['buy']['deletedeltatime'].append(order.otime - trans.otime)
            else:
                print('MISSING DELETED' + order.id)

        # Computes the time between placing and order and its execution
        if order.type in ['E', 'C']:
            trans = sorders.query_id(order.id)
            if trans.buy_sell == 'S':
                statistics['sell']['executiondeltatime'].append(order.otime - trans.otime)
                statistics['sell']['executiontime'].append(order.otime)
                if order.type == 'E':
                    statistics['sell']['executionprice'].append(trans.price)
                else:  # Execution with price
                    statistics['sell']['executionprice'].append(order.price)
                statistics['sell']['executionsize'].append(order.size)
            else:

                statistics['buy']['executiondeltatime'].append(order.otime - trans.otime)
                statistics['buy']['executiontime'].append(order.otime)

                if order.type == 'E':
                    statistics['buy']['executionprice'].append(trans.price)
                else:  # Execution with price
                    statistics['buy']['executionprice'].append(order.price)
                statistics['buy']['executionsize'].append(order.size)

    # Convert everything to numpy arrays
    for v in statistics:
        for att in statistics[v]:
            statistics[v][att] = np.array(statistics[v][att])

    return statistics


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

def log_process(statistics,log=False):
    """
    Some logging of the results

    :param statistics:
    :return:
    """
    if log:
        print('N Buy orders:', len(statistics['buy']['ordertime']))
        print('N Sell orders:', len(statistics['sell']['ordertime']))
        print('N Order Executions Sell:', len(statistics['sell']['executiontime']))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(statistics['sell']['executiontime'])))
        print('Max time to execution:', nanoseconds_to_time(np.max(statistics['sell']['executiontime'])))
        print('Min time to execution:', nanoseconds_to_time(np.min(statistics['sell']['executiontime'])))
        print('N Order Executions Buy:', len(statistics['buy']['executiontime']))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(statistics['buy']['executiontime'])))
        print('Max time to execution:', nanoseconds_to_time(np.max(statistics['buy']['executiontime'])))
        print('Min time to execution:', nanoseconds_to_time(np.min(statistics['buy']['executiontime'])))

def save_statistics(statistics, year, day, stock):
    """
    Saves the statistics in a picke file
    :param statistics:
    :return:
    """
    print(f'STOCK= {stock}')
    wfile = open(f'{analysispath}/{ITCH_days[year][day]}-{stock}-ActivityStatistics.pkl', 'wb')
    pickle.dump(statistics, wfile)
    wfile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Year of the analysis", type=str, default='2017G')
    parser.add_argument('--init', help="Initial Day", type=int, default=0)
    parser.add_argument('--day', help="One specific day", type=int, default=None)
    parser.add_argument('--nstocks', help="Number of stocks to analyze", type=int, default=50)
    parser.add_argument('--stock', help="One specific stock", type=str, default=None)
    parser.add_argument('--istock', help="Number of stocks to analyze", type=int, default=0)
    parser.add_argument('--plot', help="Plot graphs of the statistics", action='store_true', default=False)
    parser.add_argument('--log', help="Activity log", action='store_true', default=False)
    args = parser.parse_args()


    if 'G' in args.year:
        analysispath = datapath + '/GIS/Analysis'
    else:
        analysispath = datapath + '/Analysis'


    if args.day is not None:

        itchday = ITCH_days[args.year][args.day]
        if args.stock is not None:
            statistics = order_statistics(args.year, args.day, args.stock)
            log_process(statistics, args.log)
            save_statistics(statistics, args.year, args.day, args.stock)
            if args.plot:
                plot_statistics(statistics)
        else:
            sstocks = Stock(num=args.nstocks)
            for stock in sstocks.get_list_stocks():
                statistics = order_statistics(args.year, args.day, stock)
                log_process(statistics, args.log)
                save_statistics(statistics, args.year, args.day, stock)

    else:
        for day in range(args.init, len(ITCH_days[args.year])):
            if args.stock is not None:
                statistics = order_statistics(args.year, day, args.stock)
                log_process(statistics, args.log)
                save_statistics(statistics, args.year, day, args.stock)
            else:
                sstocks = Stock(num=args.nstocks)
                for stock in sstocks.get_list_stocks():
                    statistics = order_statistics(args.year, day, stock)
                    log_process(statistics, args.log)
                    save_statistics(statistics, args.year, day, stock)
