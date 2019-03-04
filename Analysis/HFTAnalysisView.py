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

import pickle

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')
    parser.add_argument('--day', help="dia del anyo", type=int, default=0)
    parser.add_argument('--stock', help="Stock del analisis", default='GOOGL')

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
    for st in stat:
        plt.title(f'buy - {st} / DAY: {ITCH_days[args.year][day]} STOCK: {stock}')
        for v in timelines[:-1]:
            sns.distplot(statistics[v]['buy'][st], hist=True, norm_hist=True, bins=10,
                         label=ntimelines[timelines.index(v)])
        plt.legend()
        plt.show()

        plt.title(f'sell - {st} / DAY: {ITCH_days[args.year][day]} STOCK: {stock}')
        for v in timelines[:-1]:
            sns.distplot(statistics[v]['sell'][st], hist=True, norm_hist=True, bins=10,
                         label=ntimelines[timelines.index(v)])
        plt.legend()
        plt.show()
