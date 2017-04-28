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

__author__ = 'bejar'


import gzip

import numpy as np

from FSociety.Util import datapath, ITCH_days, NASDAQ_actions, time_to_nanoseconds, Company, ITCHtime, Stock

__author__ = 'bejar'

if __name__ == '__main__':

    messages = ['F', 'A', 'E', 'C', 'X', 'D', 'U', 'P']
    i_time = time_to_nanoseconds(9, 30)
    f_time = time_to_nanoseconds(16)
    # st_time = time_to_nanoseconds(0, 10)

    sstocks = Stock()
    cpny = Company()

    lcounts = {}
    totalcounts = {}
    for m in messages:
        totalcounts[m] = np.zeros(len(ITCH_days['2015']), dtype=int)
    for stock in sstocks.get_list_stocks():
        lcounts[stock] = {}
        for m in messages:
            lcounts[stock][m] = np.zeros(len(ITCH_days['2015']), dtype=int)
        for i, day in enumerate(ITCH_days['2015']):
            print(stock, day)
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
            print('{}, {}, {}, {:d}, {:d}, {:d}'.format(stock, m, NASDAQ_actions[m], np.min(lcounts[stock][m]), np.max(lcounts[stock][m]), int(np.mean(lcounts[stock][m])) ) )
            totalcounts[m] += lcounts[stock][m]

    print('-----------------------')

    print('TOTALS')

    for m in messages:
        print('{}, {}, {:d}, {:d}, {:d}'.format(m, NASDAQ_actions[m], np.min(totalcounts[m]),
                                                np.max(totalcounts[m]), int(np.mean(totalcounts[m])) ) )