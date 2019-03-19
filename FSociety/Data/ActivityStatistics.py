"""
.. module:: ActivityStatistics

ActivityStatistics
*************

:Description: ActivityStatistics

    

:Authors: bejar
    

:Version: 

:Created on: 18/03/2019 10:45 

"""

from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter
from FSociety.Config import datapath, ITCH_days, ntimelines
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from FSociety.Util import nanoseconds_to_time, capped_prices
import pickle
from collections import Counter
import pandas as pd


__author__ = 'bejar'


def plot_tscale():
    plt.plot([3,3],[0,0.1], 'r')
    plt.plot([6,6],[0,0.1], 'r')
    plt.plot([9,9],[0,0.1], 'r')
    plt.plot([10,10],[0,0.05], 'g')
    plt.plot([11,11],[0,0.05], 'g')

def normalize_counter(counter):
    tsum = np.sum([v for v in counter.values()])
    dcounter = dict(counter)
    for v in dcounter:
        dcounter[v]=dcounter[v]/tsum
    return dcounter

class ActivityStatistics:
    """
    Class to store the activity statistics of a stock
    """

    statistics = None
    year=None
    day=None
    stock=None
    maxlen = None
    ntimelines = None
    itchday= None
    heat=False

    def __init__(self, year, day=None, stock=None, heat=False):
        """

        :param year:
        :param day:
        :param stock:
        """
        self.year = year
        self.day = day
        self.stock = stock
        self.heat=heat

        if 'G' in year:
            analysispath = datapath + '/GIS/Analysis'
        else:
            analysispath = datapath + '/Analysis'

        if day is None:
            # Statistics for a month
            self.ntimelines = ntimelines.copy()
            self.ntimelines.reverse()
            dstat = {'buy':{'executiondeltatime':[], 'deletedeltatime':[]}, 'sell':{'executiondeltatime':[], 'deletedeltatime':[]}}
            mxlens = 0
            mxlenb = 0
            for day in ITCH_days[year]:
                rfile = open(f'{analysispath}/{day}-{stock}-ActivityStatistics.pkl', 'rb')
                statistics = pickle.load(rfile)
                rfile.close()

                if heat:
                    ldata = np.trunc(np.log10(statistics['buy']['executiondeltatime']))
                    excount = normalize_counter(Counter(ldata))
                    mxlens = len(excount) if len(excount) > mxlens else mxlens
                    dstat['buy']['executiondeltatime'].append(excount)

                    ldata = np.trunc(np.log10(statistics['sell']['executiondeltatime']))
                    excount = normalize_counter(Counter(ldata))
                    mxlenb = len(excount) if len(excount) > mxlenb else mxlenb
                    dstat['sell']['executiondeltatime'].append(excount)

                    ldata = np.trunc(np.log10(statistics['buy']['deletedeltatime']))
                    excount = normalize_counter(Counter(ldata))
                    dstat['buy']['deletedeltatime'].append(excount)

                    ldata = np.trunc(np.log10(statistics['sell']['deletedeltatime']))
                    excount = normalize_counter(Counter(ldata))
                    dstat['sell']['deletedeltatime'].append(excount)
                else:
                    dstat['buy']['executiondeltatime'].append(np.log10(statistics['buy']['executiondeltatime']))
                    dstat['sell']['executiondeltatime'].append(np.log10(statistics['sell']['executiondeltatime']))
                    dstat['buy']['deletedeltatime'].append(np.log10(statistics['buy']['deletedeltatime']))
                    dstat['sell']['deletedeltatime'].append(np.log10(statistics['sell']['deletedeltatime']))

            self.statistics = dstat
            if heat:
                self.maxlen= np.max([mxlenb, mxlens])
        else:
            self.itchday = ITCH_days[year][day]
            rfile = open(f'{analysispath}/{ITCH_days[year][day]}-{stock}-ActivityStatistics.pkl', 'rb')
            self.statistics = pickle.load(rfile)
            rfile.close()



    def log(self):
        """
        Data info
        :return:
        """
        if self.day is None:
            raise NameError('Montly data are not loaded')
        print('N Buy orders:', len(self.statistics['buy']['ordertime']))
        print('N Sell orders:', len(self.statistics['sell']['ordertime']))
        print('N Order Executions Sell:', len(self.statistics['sell']['executiondeltatime']))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(self.statistics['sell']['executiondeltatime'])))
        print('Max time to execution:', nanoseconds_to_time(np.max(self.statistics['sell']['executiondeltatime'])))
        print('Min time to execution:', nanoseconds_to_time(np.min(self.statistics['sell']['executiondeltatime'])))
        print('N Order Executions Buy:', len(self.statistics['buy']['executiondeltatime']))
        print('Mean time to execution:', nanoseconds_to_time(np.mean(self.statistics['buy']['executiondeltatime'])))
        print('Max time to execution:', nanoseconds_to_time(np.max(self.statistics['buy']['executiondeltatime'])))
        print('Min time to execution:', nanoseconds_to_time(np.min(self.statistics['buy']['executiondeltatime'])))



    def plot_deltatime_heatmap(self, side='buy', type='execution'):
        """
        Plots a heatmap of a delta time
        side = ['buy', 'sell']
        type = ['execution', 'delete']
        :return:
        """
        if self.day is not None:
            raise NameError('Montly data are not loaded')
        if side not in ['buy', 'sell']:
            raise NameError('Wrong side value')
        if type not in ['execution', 'delete']:
            raise NameError('Wrong type value')

        dexcount = {'day': [], 'time': [], 'val': []}
        lcount = self.statistics[side][f'{type}deltatime']

        for day, count in zip(ITCH_days[self.year], lcount):
            for v in range(4, self.maxlen):
                dexcount['day'].append(day)
                dexcount['time'].append(v)
                if v in count:
                    dexcount['val'].append(count[v])
                else:
                    dexcount['val'].append(0)

        dfexcount = pd.DataFrame(dexcount)

        f, ax = plt.subplots(figsize=(9, 6))
        sns.heatmap(dfexcount.pivot('time', 'day', 'val'), annot=False, linewidths=.5, ax=ax,
                    yticklabels=self.ntimelines, cmap='Reds',vmax=0.5,vmin=0)
        plt.title(f'{self.year}/month {side} delta {type} time distribution {self.stock}', fontsize=15)


    def plot_deltatime_violinplot(self, side='buy', type='execution'):
        """
        Plots a heatmap of a delta time
        side = ['buy', 'sell']
        type = ['execution', 'delete']
        :return:
        """
        if self.day is not None:
            raise NameError('Montly data are not loaded')
        if side not in ['buy', 'sell']:
            raise NameError('Wrong side value')
        if type not in ['execution', 'delete']:
            raise NameError('Wrong type value')

        dexcount = {'day': [], 'time': []}
        lcount = self.statistics[side][f'{type}deltatime']

        for day, count in zip(ITCH_days[self.year], lcount):
                dexcount['day'].extend([day]*len(count))
                dexcount['time'].extend(count)

        dfexcount = pd.DataFrame(dexcount)

        f, ax = plt.subplots(figsize=(16, 6))
        sns.violinplot(x='day', y='time', data=dfexcount)
        plt.title(f'{self.year}/month {side} delta {type} time distribution {self.stock}', fontsize=15)


    def plot_statistics_deltatimes(self, type='sell',kde=False, bins=10):
        """
        deltatime statistics
        type = ['buy', 'sell', 'delete', 'all'
        :param self:
        :param istat:
        :return:
        """
        if self.day is None:
            raise NameError('Montly data are not loaded')
        if type == 'sell':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(np.log10(self.statistics['sell']['executiondeltatime']), kde=kde, bins=bins, norm_hist=True)
            plot_tscale()
            plt.title(f'Log plot of Sell execution delta time {self.itchday} {self.stock}', fontsize=20)
        elif type == 'buy':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(np.log10(self.statistics['buy']['executiondeltatime']), kde=kde, bins=bins, norm_hist=True)
            plot_tscale()
            plt.title(f'Log plot of Buy execution time {self.itchday} {self.stock}', fontsize=20)
        elif type == 'delete':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(np.log10(self.statistics['buy']['deletedeltatime']), kde=kde, bins=bins, norm_hist=True, label='Buy')
            ax = sns.distplot(np.log10(self.statistics['sell']['deletedeltatime']), kde=kde, bins=bins, norm_hist=True, label='Sell')
            plot_tscale()
            plt.legend()
            plt.title(f'Log plot of deletion time (Buy/Sell) {self.itchday} {self.stock}', fontsize=20)

        elif type == 'all':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(np.log10(self.statistics['sell']['executiondeltatime']), kde=True, hist=False, color='r',
                              label='Exec Buy')
            ax = sns.distplot(np.log10(self.statistics['buy']['executiondeltatime']), kde=True, hist=False, color='g',
                              label='Exec Sell')
            ax = sns.distplot(np.log10(self.statistics['buy']['deletedeltatime']), kde=True, hist=False, color='b',
                              label='Del Buy')
            ax = sns.distplot(np.log10(self.statistics['sell']['deletedeltatime']), kde=True, hist=False, color='k',
                              label='Del Sell')
            plt.legend()
            plot_tscale()
            plt.title(f'ExSell/ExBuy/Deletion time {self.itchday} {self.stock}', fontsize=20)


    def plot_statistics_prices(self, type='order'):
        """
        Prices statistics

        type = ['order', 'execution']
        :param self:
        :param side:
        :return:
        """
        if self.day is None:
            raise NameError('Montly data are not loaded')
        if type == 'execution':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(capped_prices(self.statistics['sell']['executionprice']), kde=True, hist=False, color='r',
                              label='Sell')
            ax = sns.distplot(capped_prices(self.statistics['buy']['executionprice']), kde=True, hist=False, color='g',
                              label='Buy')
            plt.legend()
            plt.title(f'Sell/Buy execution prices distribution {self.itchday} {self.stock}', fontsize=20)
        elif type == 'order':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(capped_prices(self.statistics['sell']['orderprice']), kde=True, hist=False, color='r',
                              label='Sell')
            ax = sns.distplot(capped_prices(self.statistics['buy']['orderprice']), kde=True, hist=False, color='g', label='Buy')
            plt.legend()
            plt.title(f'Sell/Buy orders prices distribution {self.itchday} {self.stock}', fontsize=20)
        # if istat == 1:
        #     fig = plt.figure(figsize=(12, 8))
        #     ax = sns.distplot(capped_prices(statistics['sell']['executionprice']), kde=self.kde, bins=self.bins, norm_hist=True)
        #     plt.title(f'Orders Sell execution price {itchday} {self.stock}', fontsize=20)
        # if istat == 1:
        # fig = plt.figure(figsize=(12, 8))
        # ax = sns.distplot(capped_prices(statistics['buy']['executionprice']), kde=self.kde, bins=self.bins, norm_hist=True)
        # plt.title(f'Orders Buy execution price {itchday} {self.stock}', fontsize=20)
        # plt.show()


    def plot_statistics_sizes(self, type='order', bins=10):
        """
        Sizes statistics
        :param self:
        :param type:
        :return:
        """
        if self.day is None:
            raise NameError('Montly data are not loaded')
        if type == 'execution':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(capped_prices(self.statistics['sell']['executionsize']), kde=False, bins=bins, hist=True,
                              color='r',
                              label='Sell')
            ax = sns.distplot(capped_prices(self.statistics['buy']['executionsize']), kde=False, bins=bins, hist=True,
                              color='g',
                              label='Buy')
            plt.title(f'Sell/Buy execution sizes distribution {self.itchday} {self.stock}', fontsize=20)
            plt.legend()
        elif type == 'order':
            fig = plt.figure(figsize=(12, 8))
            ax = sns.distplot(capped_prices(self.statistics['sell']['ordersize']), kde=False, bins=bins, hist=True, color='r', label='Sell')
            ax = sns.distplot(capped_prices(self.statistics['buy']['ordersize']), kde=False, bins=bins, hist=True, color='g', label='Buy')
            plt.title(f'Sell/Buy orders sizes distribution {self.itchday} {self.stock}', fontsize=20)
            plt.legend()




    def plot_price_evolution(self):
        """
        Whole session price evolution
        :param self:
        :return:
        """
        if self.day is None:
            raise NameError('daily data are not loaded')
        fig = plt.figure(figsize=(14, 8))
        plt.plot(self.statistics['sell']['ordertime'], self.statistics['sell']['orderprice'], color='r')
        plt.plot(self.statistics['buy']['ordertime'], self.statistics['buy']['orderprice'], color='g')
        plt.scatter(self.statistics['sell']['executiontime'], self.statistics['sell']['executionprice'], marker='o', color='y',
                    s=self.statistics['sell']['executionsize'])
        plt.scatter(self.statistics['buy']['executiontime'], self.statistics['buy']['executionprice'], marker='o', color='b',
                    s=self.statistics['buy']['executionsize'])

        plt.title(f'Order Sell/Buy price evolution ', fontsize=20)

