"""
.. module:: HFTAnalysis

HFTAnalysis
*************

:Description: HFTAnalysis

    

:Authors: bejar
    

:Version: 

:Created on: 04/03/2019 7:46 

"""

import argparse
from FSociety.Data.TimeLineSummary import order_exec_analysis
from FSociety.Config import datapath, ITCH_days
from FSociety.Data import Stock
from FSociety.Util import now
import pickle
from FSociety.Data.TimeLineSummary import timelines, ntimelines, stat
import seaborn as sns
import matplotlib.pyplot as plt

__author__ = 'bejar'


def save_analysis(year, day, stock, market):
    statistics = order_exec_analysis(year, day, stock, logging=args.log, market=market)
    wfile = open(f'{analysispath}/{ITCH_days[year][day]}-{stock}-HFTStatistics.pkl', 'wb')
    pickle.dump(statistics, wfile)
    wfile.close()
    return statistics


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Year of the analysis", type=str, default='2017G')
    parser.add_argument('--nstocks', help="Number of stocks to analyze", type=int, default=50)
    parser.add_argument('--init', help="Initial Day", type=int, default=0)
    parser.add_argument('--log', help="Prints order executions", action='store_true', default=False)
    parser.add_argument('--plot', help="Plots final results", action='store_true', default=False)
    parser.add_argument('--day', help="One specific dat", type=int, default=None)
    parser.add_argument('--stock', help="One specific stock", default=None)
    parser.add_argument('--istock', help="Number of stocks to analyze", type=int, default=0)
    parser.add_argument('--market', help="Process only market hours", action='store_true', default=False)

    args = parser.parse_args()
    year = args.year
    sstocks = Stock(num=args.nstocks)

    if 'G' in year:
        # lfiles = [f'/S{day}-v50.txt.gz' for day in ITCH_days[year]]
        # datapath = datapath + '/GIS/'
        analysispath = datapath + '/GIS/Analysis'
    else:
        # lfiles = [f'{day}.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]
        analysispath = datapath + '/Analysis'

    if args.day is None:
        for day in range(args.init, len(ITCH_days[args.year])):
            now()
            print(f'DAY: {ITCH_days[args.year][day]}')
            for stock in sstocks.get_list_stocks()[args.istock:]:
                print(f'STOCK= {stock}')
                save_analysis(args.year, day, stock, market=args.market)

    else:
        print(f'DAY: {ITCH_days[args.year][args.day]}')
        if args.stock is None:
            raise NameError('The stock is missing')
        print(f'STOCK= {args.stock}')
        statistics = save_analysis(args.year, args.day, args.stock, market=args.market)
        # statistics = order_exec_analysis(args.year, args.day, args.stock, logging=args.log, market=args.market)
        # wfile = open(f'{analysispath}/{ITCH_days[args.year][args.day]}-{args.stock}-HFTStatistics.pkl', 'wb')
        # pickle.dump(statistics, wfile)
        # wfile.close()
        if args.plot:
            for st in stat:
                plt.title(f'buy - {st} / DAY: {ITCH_days[args.year][args.day]} STOCK: {args.stock}')
                for v in timelines[:-1]:
                    sns.distplot(statistics[v]['buy'][st], hist=True, norm_hist=True, bins=10,
                                 label=ntimelines[timelines.index(v)])
                plt.legend()
                plt.show()

                plt.title(f'sell - {st} / DAY: {ITCH_days[args.year][args.day]} STOCK: {args.stock}')
                for v in timelines[:-1]:
                    sns.distplot(statistics[v]['sell'][st], hist=True, norm_hist=True, bins=10,
                                 label=ntimelines[timelines.index(v)])
                plt.legend()
                plt.show()
