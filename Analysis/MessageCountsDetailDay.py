"""
.. module:: MessageCountsDetail

MessageCountsDetail
*************

:Description: MessageCountsDetail

  Detailed counted of messages for all the days (available) of a year    

:Authors: bejar
    

:Version: 

:Created on: 21/04/2017 9:57 

"""



import gzip

import numpy as np
import argparse

from FSociety.Util import time_to_nanoseconds
from FSociety.Data import Stock, Company
from FSociety.Config import datapath, ITCH_days, NASDAQ_actions
from FSociety.ITCH import ITCHtime

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default="")

    args = parser.parse_args()
    year = str(args.year)

    if year == '':
        year = '2015'

    messages = ['F', 'A', 'E', 'C', 'X', 'D', 'U', 'P']
    i_time = time_to_nanoseconds(9, 30)
    f_time = time_to_nanoseconds(16)
    # st_time = time_to_nanoseconds(0, 10)

    sstocks = Stock(fast=True)
    cpny = Company()

    lcounts = {}
    totalcounts = {}
    for m in messages:
        totalcounts[m] = np.zeros(len(ITCH_days[year]), dtype=int)

    for stock in sstocks.get_list_stocks():
        lcounts[stock] = {}
        for m in messages:
            lcounts[stock][m] = np.zeros(len(ITCH_days[year]), dtype=int)
        for i, day in enumerate(ITCH_days[year]):
            try :
                rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')
                for mess in rfile:
                    try:
                        data = mess.split(',')
                        order = data[2].strip()
                        timestamp = ITCHtime(int(data[1].strip()))
                        if i_time <= timestamp.itime < f_time:
                           lcounts[stock][order][i] += 1
                    except IndexError:
                        print(mess)
            except FileNotFoundError:
                pass


        cp = cpny.get_company(stock)


        for m in messages:
            print('{:5s} {:3s} '.format(stock,m), end=" ")
            for i, day in enumerate(ITCH_days[year]):
                print('{:7d} '.format(lcounts[stock][m][i]), end=" ")
                totalcounts[m][i] += lcounts[stock][m][i]
            print ()

    print('-----------------------')

    print('TOTALS')

    for m in messages:
        print('TOTAL {:3s} '.format(m), end=" ")
        for i, day in enumerate(ITCH_days[year]):
            print('{:7d} '.format(totalcounts[m][i]), end=" ")
        print ()
