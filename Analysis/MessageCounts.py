"""
.. module:: MessageCounts

MessageCounts
*************

:Description: MessageCounts

    Outputs the stocks in NYSE and NASDAQ that have more than 250 messages for each 10 minutes period for all the
    days (available) of a year

:Authors: bejar
    

:Version: 

:Created on: 19/04/2017 8:35 

"""
import gzip

import numpy as np
import argparse

from FSociety.Util import now, time_to_nanoseconds
from FSociety.Data import Stock, Company
from FSociety.Config import datapath, ITCH_days

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default=None)

    args = parser.parse_args()
    year = args.year
    i_time = time_to_nanoseconds(9, 30)
    f_time = time_to_nanoseconds(16)
    st_time = time_to_nanoseconds(0, 10)

    sstocks = Stock()
    cpny = Company()

    lcounts = {}
    counter = 0
    for stock in sstocks.get_list_stocks():
        lcounts[stock] = []
        for day in ITCH_days[year]:
            rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')
            count = np.zeros(39)
            for mess in rfile:
                data = mess.split(',')
                timestamp = ITCHtime(int(data[1].strip()))
                order = data[2].strip()
                ORN = data[3].strip()
                if i_time <= timestamp.itime < f_time:
                    bucket = int(timestamp.itime/st_time) - 57
                    count[bucket] += 1

            lcounts[stock].append(count)
        allsup = True
        mincount = 10000000000000000000
        maxcount = 1
        for cnt in lcounts[stock]:
            allsup = allsup and (np.sum(cnt > 600) == cnt.shape[0])
            if np.min(cnt) < mincount:
                mincount = np.min(cnt)
            if np.max(cnt) > maxcount:
                maxcount = np.max(cnt)
        meancount = np.mean(np.array(lcounts[stock]))
        if allsup:
            cp = cpny.get_company(stock)
            if cp is not None and cp[3] in ['NYSE', 'NASDAQ']:
                print("{}, {}, {}, {}, {}, {:d}, {:d}, {:d}".format(stock, cp[0], cp[1], cp[2], cp[3],
                                                                    int(mincount), int(maxcount), int(meancount)))
                counter += 1
    print(counter)

