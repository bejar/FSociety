"""
.. module:: test

test
*************

:Description: test

    

:Authors: bejar
    

:Version: 

:Created on: 15/07/2016 12:47 

"""

from ITCHbin import ITCHv5
from ITCHtime import ITCHtime
from Util import now
import pandas as pd
pd.__version__ = '0.18'
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from Constants import ITCH_files, datapath

__author__ = 'bejar'



def summarize_stock_action_agent(structure):
    """
    Summarizes the structure stock-action-agent
    :param structure:
    :return:
    """

    for stock in structure:
        for action in structure[stock]:
            print(stock.strip(), action, len(structure[stock][action]))
    print('----------------------------------------------------------')


if __name__ == '__main__':
    filename = ITCH_files[0]
    nrec = 0
    dataset = ITCHv5(datapath + filename)

    gendata = dataset.records()

    actionsdic = {}

    stockdic = {}
    agentsset = set()

    buy = np.zeros(24)
    sell = np.zeros(24)
    uabuy = np.zeros(24)
    uasell = np.zeros(24)

    i = 0
    now()
    ophour = 0
    uophour = 0
    print(filename)
    for g in gendata:
        action = dataset.to_string(g[0])
        if action == 'F':
            stock = dataset.to_string(g[7])
            agent = dataset.to_string(g[9])
            order = dataset.to_string(g[5])
            itime = ITCHtime(g[3])

            if order == 'B':
                buy[itime.hours] += 1
            else:
                sell[itime.hours] += 1
            # if not agent in agentsset:
            #     print(agent)
            # if not stock in stockdic:
            #     stockdic[stock] = {}
            # if not order in stockdic[stock]:
            #     stockdic[stock][order] = {}
            # if not agent in stockdic[stock][order]:
            #     stockdic[stock][order][agent] = 0
            #
            # stockdic[stock][order][agent] += 1

            if itime.hours != ophour:
                print('-----> H:', ophour, 'B:',buy[ophour], 'S:',sell[ophour])
                ophour = itime.hours

        if action == 'A':
            stock = dataset.to_string(g[7])
            order = dataset.to_string(g[5])
            itime = ITCHtime(g[3])

            if order == 'B':
                uabuy[itime.hours] += 1
            else:
                uasell[itime.hours] += 1
            # if not agent in agentsset:
            #     print(agent)
            # if not stock in stockdic:
            #     stockdic[stock] = {}
            # if not order in stockdic[stock]:
            #     stockdic[stock][order] = {}
            # if not agent in stockdic[stock][order]:
            #     stockdic[stock][order][agent] = 0
            #
            # stockdic[stock][order][agent] += 1

            if itime.hours != uophour:
                print('U----> H:', ophour, 'B:', uabuy[ophour], 'S:', uasell[ophour])
                uophour = itime.hours

        if action == 'S':
            itime = ITCHtime(g[3])
            msg = dataset.to_string(g[4])
            print('-----> SYSTEM:', i, g[3], itime.to_string(), msg)

        if i > 1000000:
            nrec += i
            print(i, nrec, g[3], itime.to_string())
            #summarize_stock_action_agent(stockdic)
            # for v in actionsdic:
            #     print(v, actionsdic[v])
            #     print('##################################')
            i = 0
        i += 1


        # line = [dataset.to_string(r) for r in g]
        # print(line)

    print(nrec+i)
    now()
    # for v in actionsdic:
    #     print(v, actionsdic[v])
    #summarize_stock_action_agent(stockdic)

    fig = plt.figure()
    fig.set_figwidth(6)
    fig.set_figheight(4)

    rvals = [v for v in range(24)]
    ax = fig.add_subplot(2, 2, 1)
    sn.barplot(rvals, buy)
    ax = fig.add_subplot(2, 2, 2)
    sn.barplot(rvals,sell)
    ax = fig.add_subplot(2, 2, 3)
    sn.barplot(rvals, uabuy)
    ax = fig.add_subplot(2, 2, 4)
    sn.barplot(rvals, uasell)
    plt.show()
