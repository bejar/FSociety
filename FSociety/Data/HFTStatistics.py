"""
.. module:: HFTStatistics

HFTStatistics
*************

:Description: HFTStatistics

    

:Authors: bejar
    

:Version: 

:Created on: 18/03/2019 9:51 

"""
from FSociety.ITCH import ITCHtime
from FSociety.Config import datapath, ITCH_days, timelines, ntimelines, stat
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import pandas as pd

__author__ = 'bejar'

class HFTStatistics:
    """
    Stores the statistics for a day of a stock
    """

    statistics = None
    dtimelines = None
    dntimelines = None
    merge = False
    hft = False
    year = None
    day = None
    stock = None

    def __init__(self, year, day, stock, merge=False, hft=False):
        """

        :param year:
        :param day:
        :param stock:
        :param merge:
        :param hft:
        """
        if 'G' in year:
            analysispath = datapath + '/GIS/Analysis'
        else:
            analysispath = datapath + '/Analysis'


        self.year= year
        self.day = day
        self.stock = stock

        rfile = open(f'{analysispath}/{ITCH_days[year][day]}-{stock}-HFTStatistics.pkl', 'rb')
        self.statistics = pickle.load(rfile)
        rfile.close()

        print(f'DAY: {ITCH_days[year][day]} STOCK {stock}')
        if merge:
            dtimelines = [1_000_000_000, 1_000_000, 0]
            dntimelines =  ['inf-1s', '1s-1ms', '1ms-0']
            mergeintervals = [[10_000_000_000], [100_000_000, 10_000_000], [100_000, 10_000]]
            for st in stat:
                for mf, mt in zip(mergeintervals,dtimelines):
                    for m in mf:
                        self.statistics[mt]['buy'][st] = np.append( self.statistics[mt]['buy'][st], self.statistics[m]['buy'][st])
                        self.statistics[mt]['sell'][st] = np.append(self.statistics[mt]['sell'][st], self.statistics[m]['sell'][st])
        else:
            dtimelines = timelines
            dntimelines = ntimelines

        if hft:
            if merge:
                dtimelines = dtimelines[1:]
                dntimelines =  dntimelines[1:]
            else:
                dtimelines = dtimelines[2:]
                dntimelines =  dntimelines[2:]

        self.dtimelines = dtimelines
        self.dntimelines = dntimelines


    def single_distplot(self, side, statistic, bins=10, kde=False):
        """
        Distribution plot
        :return:
        """
        fig = plt.figure(figsize=(12, 8))
        plt.title(f'buy - {statistic} / DAY: {ITCH_days[self.year][self.day]} STOCK: {self.stock}')
        for v in self.dtimelines:
            sns.distplot(self.statistics[v][side][statistic], hist=True, norm_hist=True, bins=bins, kde=kde,
                         kde_kws={'cut': 0},
                         label=self.dntimelines[self.dtimelines.index(v)])
        plt.legend()


    def pair_plot(self, lvars, side, bins=10, kde=False):
        """
        Plots the pair plots of the variables
        :param data:
        :param lvars:
        :param year:
        :param day:
        :param stock:
        :param bins:
        :param kde:
        :return:
        """
        ddata = {s:np.zeros(0) for s in stat}
        ddata[f'time-{self.stock}-{ITCH_days[self.year][self.day]}'] = []
        for v in self.dtimelines:
            for s in stat:
                ddata[s] = np.append(ddata[s], self.statistics[v][side][s])
            ddata[f'time-{self.stock}-{ITCH_days[self.year][self.day]}'].extend([self.dntimelines[self.dtimelines.index(v)]]*self.statistics[v][side]['gap'].shape[0])
        data = pd.DataFrame(ddata)
        fig = plt.figure(figsize=(12, 8))
        g = sns.PairGrid(data,vars=lvars, hue=f'time-{self.stock}-{ITCH_days[self.year][self.day]}')
        if kde:
            g = g.map_diag(sns.kdeplot,cut=0)
        else:
            g = g.map_diag(plt.hist,bins=bins)
        g = g.map_offdiag(plt.scatter)
        g.add_legend()

