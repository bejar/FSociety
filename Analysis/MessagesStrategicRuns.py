"""
.. module:: MessagesStrategicRuns

MessagesStrategicRuns
*************

:Description: MessagesStrategicRuns

 Counts the length and number of strategic runs    

:Authors: bejar
    

:Version: 

:Created on: 29/05/2017 9:48 

"""

import gzip

import numpy as np
import argparse
import seaborn as sns
import matplotlib.pyplot as plt

from FSociety.Util import time_to_nanoseconds
from FSociety.Data import Stock
from FSociety.Config import datapath, ITCH_days
from FSociety.ITCH import ITCHtime
from collections import Counter

__author__ = 'bejar'


def find_last_bid(lmsg):
    """
    Finds the position of the last A, F or U message in a sequence of messages
    lmsg always has a message A at its begginning

    :return:
    """
    for i in range(len(lmsg) - 1, 0, -1):
        if lmsg[i][1] in ['A', 'F', 'U']:
            return i

def compute_counts(lc):
    """
    Prints a list of counts from 3 to 99 and 100+
    :param lc:
    :return:
    """
    vcount = np.zeros(101, dtype=int)
    c = Counter(lc)

    for v in range(3,100):
        vcount[v]= c[v]

    lesscommon = c.most_common()[-1][0]
    if lesscommon >= 100:
        for v in range(100, lesscommon+1):
            vcount[100] += c[v]

    return vcount


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default="")

    args = parser.parse_args()
    year = str(args.year)

    if year == '':
        year = '2016'

    i_time = time_to_nanoseconds(9, 30)
    f_time = time_to_nanoseconds(16)

    sstock = Stock(fast=True)


    mgap = 1e+8
    detail = {}
    for stock in sorted(sstock.get_list_stocks()):
        detail[stock] = {}
        for day in ITCH_days[year]:
            detail[stock][day] = 0
    aggrday = {}

    for day in ITCH_days[year]:
        runlengths = []
        runlengthspass = []
        runlengthsact = []
        runtime = []
        print(day)
        for stock in sorted(sstock.get_list_stocks()):
            print(stock)
            rfile = gzip.open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv.gz', 'rt')
            addorders = {}
            for mess in rfile:
                try:
                    data = mess.strip().split(',')
                    order = data[2].strip()
                    timestamp = ITCHtime(int(data[1].strip()))
                    ORN = data[3].strip()
                    # print(order, ORN)
                    if order in ['A', 'F']:
                        bos = data[5].strip()
                        nshares = int(data[6].strip())
                        if order == 'A':
                            price = float(data[7].strip())
                        else:
                            price = float(data[8].strip())
                        addorders[ORN] = [[timestamp.itime, order, bos, price, nshares, ORN]]
                    if order in ['U']:
                        nORN = data[4].strip()
                        nshares = int(data[5].strip())
                        price = float(data[6].strip())
                        oldorder = addorders[ORN]
                        bos = addorders[ORN][0][2]
                        oldorder.append([timestamp.itime, order, bos, price, nshares, nORN, ORN])
                        addorders[nORN] = oldorder
                        del addorders[ORN]
                    if order in ['E', 'C']:
                        price = float(data[6].strip()) if order == 'C' else 0
                        nshares = int(data[4].strip())
                        addorders[ORN].append([timestamp.itime, order, price, nshares])
                    if order in ['D']:
                        addorders[ORN].append([timestamp.itime, order])
                    if order in ['X']:
                        cancel = data[4].strip()
                        addorders[ORN].append([timestamp.itime, order, cancel])
                except IndexError:
                    print('<<', mess)
                except KeyError:
                    print('---->', ORN, order)

            # Select only groups of messages separated less than 100ms
            addpost = {}
            for o in addorders:
                tinit = addorders[o][0][0]
                tend = addorders[o][-1][0]
                if (tend - tinit) <= mgap and \
                                len(addorders[o]) > 1 and (i_time <= tinit <= f_time):
                    addpost[o] = addorders[o]

            addord = sorted([(addpost[o][0][0], addpost[o]) for o in addpost])

            lseq = []
            doneset = set()
            for i in range(len(addord)):
                if i not in doneset:
                    doneset.add(i)
                    end = False
                    # Time of the last message of the first in the sequence
                    mseq = addord[i][1]
                    tend = addord[i][1][-1][0]
                    bos = addord[i][1][0][2]  # Buy or sell
                    nshares = addord[i][1][0][4]
                    j = 0
                    while not end:
                        j += 1
                        if i + j >= len(addord):
                            end = True
                        else:
                            # Fist time of the sequence
                            tinit = addord[i + j][1][0][0]
                            if 0 <= (tinit - tend) <= mgap:
                                if addord[i + j][1][0][2] == bos and addord[i + j][1][0][4] == nshares:
                                    doneset.add(i + j)
                                    mseq.extend(addord[i + j][1])
                                    tend = addord[i + j][1][-1][0]
                                    op = addord[i + j][1][-1][1]
                                    if op in ['E', 'C']:
                                        end = True
                            else:
                                end = True
                    if len(mseq) > 2:
                        lseq.append(mseq)

            detail[stock][day] = len(lseq)
            for l in lseq:
                runlengths.append(len(l))
                if l[-1][1] in ['E', 'C']:
                    runlengthspass.append(len(l))
                if l[-1][1] in ['D']:
                    runlengthsact.append(len(l))
                runtime.append((l[-1][0]-l[0][0])/1000000.0)

        # fig = plt.figure(figsize=(12, 8))
        # ax = sns.distplot(runlengths, kde=False, norm_hist=True, bins=100)
        # plt.title('Strategic runs ' + day)
        # plt.show()
        #
        # fig = plt.figure(figsize=(12, 8))
        # ax = sns.distplot(runtime, kde=False, norm_hist=True, bins=100)
        # plt.title('Strategic runs ' + day)
        # plt.show()

        counttotal = compute_counts(runlengths)
        countactive = compute_counts(runlengthsact)
        countpassive = compute_counts(runlengthspass)
        aggrday[day] = [counttotal, countactive, countpassive]

    for stock in sorted(sstock.get_list_stocks()):
        print('{:5s} '.format(stock), end='')
        for day in ITCH_days[year]:
            print('{:7d} '.format(detail[stock][day]), end='')
        print()

    print()
    for i in range(3,101):
        print('{:3d} '.format(i), end='')
        for day in ITCH_days[year]:
            print('{:6d} {:6d} {:6d} '.format(aggrday[day][0][i], aggrday[day][1][i], aggrday[day][2][i]), end='')
        print()
