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

__author__ = 'bejar'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Year of the analysis", default='2017G')
    parser.add_argument('--nstocks', help="Number of stocks to analyze", type=int, default=50)
    parser.add_argument('--init', help="Initial Day", type=int, default=0)
    parser.add_argument('--log', help="Prints order executions", action='store_true', default=False)

    args = parser.parse_args()
    year = str(args.year)
    sstocks = Stock(num=args.nstocks)
    print(len(sstocks.sstocks))

    if 'G' in year:
        # lfiles = [f'/S{day}-v50.txt.gz' for day in ITCH_days[year]]
        # datapath = datapath + '/GIS/'
        analysispath = datapath + '/GIS/Analysis'
    else:
        # lfiles = [f'{day}.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]
        analysispath = datapath + '/Analysis'

    for day in range(len(ITCH_days[args.year])):
        now()
        print(f'DAY: {ITCH_days[args.year][day]}')
        for stock in sstocks.get_list_stocks():
            print(f'STOCK= {stock}')
            statistics = order_exec_analysis(args.year, day, stock, logging=args.log)
            wfile = open(f'{analysispath}/{ITCH_days[args.year][day]}-{stock}-HFTStatistics.pkl', 'wb')
            pickle.dump(statistics, wfile)
            wfile.close()

