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
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter, ActivityStatistics
from FSociety.Config import datapath, ITCH_days, ntimelines
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from FSociety.Util import nanoseconds_to_time, capped_prices
import pickle
from collections import Counter
import pandas as pd


__author__ = 'bejar'


def plot_statistics(statistics):
    """
    Some plot of the results
    :param statistics:
    :return:
    """
    statistics.plot_statistics_deltatimes(type='sell',kde=args.kde, bins=args.bins)
    plt.show()

    statistics.plot_statistics_deltatimes(type='buy',kde=args.kde, bins=args.bins)
    plt.show()

    statistics.plot_statistics_deltatimes(type='delete',kde=args.kde, bins=args.bins)
    plt.show()

    statistics.plot_statistics_deltatimes(type='all',kde=args.kde, bins=args.bins)
    plt.show()

    statistics.plot_statistics_prices(type='order')
    plt.show()

    statistics.plot_statistics_prices(type='execution')
    plt.show()

    statistics.plot_statistics_sizes(type='order',bins=args.bins)
    plt.show()

    statistics.plot_statistics_sizes(type='execution',bins=args.bins)
    plt.show()

    statistics.plot_price_evolution()
    plt.show()


    #
    # fig = plt.figure(figsize=(12, 8))
    # ax = sns.distplot(capped_prices(statistics['sell']['executionprice']), kde=True, hist=False, color='r',
    #                   label='Sell')
    # ax = sns.distplot(capped_prices(statistics['buy']['executionprice']), kde=True, hist=False, color='g',
    #                   label='Buy')
    # plt.legend()
    # plt.title(f'Sell/Buy execution prices distribution {itchday} {args.stock}', fontsize=20)
    # plt.show()
    #
    # fig = plt.figure(figsize=(12, 8))
    # ax = sns.distplot(capped_prices(statistics['sell']['executionsize']), kde=False, bins=args.bins, hist=True, color='r',
    #                   label='Sell')
    # ax = sns.distplot(capped_prices(statistics['buy']['executionsize']), kde=False, bins=args.bins, hist=True, color='g',
    #                   label='Buy')
    # plt.title(f'Sell/Buy execution sizes distribution {itchday} {args.stock}', fontsize=20)
    # plt.legend()
    # plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')
    parser.add_argument('--day', help="dia del anyo", type=int, default=0)
    parser.add_argument('--stock', help="Stock del analisis", default='GOOGL')
    parser.add_argument('--kde', help="Show Kernel Density Estimation", action='store_true', default=False)
    parser.add_argument('--log', help="some logging", action='store_true', default=False)
    parser.add_argument('--bins', help="Number of histogram bins", type=int, default=10)
    parser.add_argument('--month', help="Plots for all the days in a year", action='store_true', default=False)

    args = parser.parse_args()


    if not args.month:
        actstat = ActivityStatistics(args.year, args.day, args.stock)

        if args.log:
            actstat.log()

        plot_statistics(actstat)
    else:

        actstat = ActivityStatistics(args.year, day=None, stock=args.stock)
        actstat.plot_deltatime_heatmap(side='buy', type='execution')
        plt.show()
        actstat.plot_deltatime_heatmap(side='sell', type='execution')
        plt.show()
        actstat.plot_deltatime_heatmap(side='buy', type='delete')
        plt.show()
        actstat.plot_deltatime_heatmap(side='sell', type='delete')
        plt.show()



