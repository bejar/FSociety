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
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter, HFTStatistics
from FSociety.Config import datapath, ITCH_days, timelines, ntimelines, stat
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from FSociety.Data.TimeLineSummary import
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

    hftstat = HFTStatistics(year, day, stock, merge=args.merge, hft=args.hft)

    if args.single:
        for st in stat:

            hftstat.single_distplot('buy', st, bins=args.bins, kde=args.kde)
            plt.show()

            plt.show()

    if args.pair:
        lvars = ['gap','otherprice','lenbuy5','lensell5']
        hftstat.pair_plot(lvars,'buy', bins=args.bins, kde=args.kde)
        plt.show()
        hftstat.pair_plot(lvars,'sell', bins=args.bins, kde=args.kde)
        plt.show()


        
