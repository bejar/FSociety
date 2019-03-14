"""
.. module:: HFTAnalysisView

HFTAnalysisView
*************

:Description: HFTAnalysisView

    

:Authors: bejar
    

:Version: 

:Created on: 04/03/2019 8:12 

"""
import argparse

from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter
from FSociety.Config import datapath, ITCH_days
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from FSociety.Data.TimeLineSummary import timelines, ntimelines, stat
import pandas as pd

import pickle

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')
    parser.add_argument('--day', help="dia del anyo", type=int, default=0)
    parser.add_argument('--stock', help="Stock del analisis", default='GOOGL')
    parser.add_argument('--kde', help="Show Kernel Density Estimation", action='store_true', default=False)
    parser.add_argument('--bins', help="Number of histogram bins", type=int, default=10)
    parser.add_argument('--merge', help="Merge intervals", action='store_true', default=False)
    parser.add_argument('--hft', help="Just HFT times", action='store_true', default=False)
    parser.add_argument('--pair', help="pair plots", action='store_true', default=False)
    parser.add_argument('--single', help="single plots", action='store_true', default=False)

    args = parser.parse_args()
    year = args.year
    stock = args.stock
    day = args.day

    if 'G' in year:
        # lfiles = [f'/S{day}-v50.txt.gz' for day in ITCH_days[year]]
        # datapath = datapath + '/GIS/'
        analysispath = datapath + '/GIS/Analysis'
    else:
        # lfiles = [f'{day}.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]
        analysispath = datapath + '/Analysis'

    rfile = open(f'{analysispath}/{ITCH_days[args.year][day]}-{stock}-HFTStatistics.pkl', 'rb')
    statistics = pickle.load(rfile)
    rfile.close()

    print(f'DAY: {ITCH_days[args.year][day]} STOCK {stock}')
    if args.merge:
        dtimelines = [1_000_000_000, 1_000_000, 0]
        dntimelines =  ['inf-1s', '1s-1ms', '1ms-0']
        mergeintervals = [[10_000_000_000], [100_000_000, 10_000_000], [100_000, 10_000]]
        for st in stat:
            for mf, mt in zip(mergeintervals,dtimelines):
                for m in mf: 
                    statistics[mt]['buy'][st] = np.append( statistics[mt]['buy'][st], statistics[m]['buy'][st])
                    statistics[mt]['sell'][st] = np.append(statistics[mt]['sell'][st], statistics[m]['sell'][st])
    else:
        dtimelines = timelines
        dntimelines = ntimelines

    if args.hft:
        if args.merge:
            dtimelines = dtimelines[1:]
            dntimelines =  dntimelines[1:]
        else:
            dtimelines = dtimelines[2:]
            dntimelines =  dntimelines[2:]
             
            
        

    if args.single:
        for st in stat:
            plt.title(f'buy - {st} / DAY: {ITCH_days[args.year][day]} STOCK: {stock}')
            for v in dtimelines:
                sns.distplot(statistics[v]['buy'][st], hist=True, norm_hist=True, bins=args.bins,kde=args.kde,kde_kws={'cut':0}, 
                         label=dntimelines[dtimelines.index(v)])
            plt.legend()
            plt.show()

            plt.title(f'sell - {st} / DAY: {ITCH_days[args.year][day]} STOCK: {stock}')
            for v in dtimelines:
                sns.distplot(statistics[v]['sell'][st], hist=True, norm_hist=True, bins=args.bins,kde=args.kde,kde_kws={'cut':0}, 
                         label=dntimelines[dtimelines.index(v)])
            plt.legend()
            plt.show()

    if args.pair:
        lvars = ['gap','otherprice','lenbuy5','lensell5']
        ddata = {s:np.zeros(0) for s in stat}
        ddata[f'time-{stock}-{ITCH_days[args.year][day]}'] = []
        for v in dtimelines:
            for s in stat:
                ddata[s] = np.append(ddata[s], statistics[v]['buy'][s])
            ddata[f'time-{stock}-{ITCH_days[args.year][day]}'].extend([dntimelines[dtimelines.index(v)]]*statistics[v]['buy']['gap'].shape[0])

        data = pd.DataFrame(ddata)
            
        g = sns.PairGrid(data,vars=lvars, hue=f'time-{stock}-{ITCH_days[args.year][day]}')
        if args.kde:
            g = g.map_diag(sns.kdeplot,cut=0)
        else:
            g = g.map_diag(plt.hist,bins=args.bins)
        g = g.map_offdiag(plt.scatter)
        g.add_legend()
        plt.show()
            
        ddata = {s:np.zeros(0) for s in stat}
        ddata[f'time-{stock}-{ITCH_days[args.year][day]}'] = []
        for v in dtimelines:
            for s in stat:
                ddata[s] = np.append(ddata[s], statistics[v]['sell'][s])
            ddata[f'time-{stock}-{ITCH_days[args.year][day]}'].extend([dntimelines[dtimelines.index(v)]]*statistics[v]['sell']['gap'].shape[0])

        data = pd.DataFrame(ddata)
            
        g = sns.PairGrid(data,vars=lvars, hue=f'time-{stock}-{ITCH_days[args.year][day]}')
        if args.kde:
            g = g.map_diag(sns.kdeplot,cut=0)
        else:
            g = g.map_diag(plt.hist,bins=args.bins)
        g = g.map_offdiag(plt.scatter)
        g.add_legend()
        plt.show()
 
        
