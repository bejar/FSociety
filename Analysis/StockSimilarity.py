"""
.. module:: StockSimilarity

StockSimilarity
*************

:Description: StockSimilarity

    Similarity among stocks according to the delete times

:Authors: bejar
    

:Version: 

:Created on: 06/10/2016 11:24 

"""
from Util import datapath, StockOrders, ITCH_days,  nanoseconds_to_time, Company, ITCHtime, capped_prices, Stock, hellinger_distance

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import MDS, SpectralEmbedding

pd.__version__ = '0.18'

from mpl_toolkits.mplot3d import Axes3D


__author__ = 'bejar'

if __name__ == '__main__':
    sstock = Stock()
    cpny = Company()
    day = ITCH_days[0]
    dhistoD = {}
    dhistoS = {}
    dhistoB = {}
    mxhval = 16  # Max possible time interval

    lstocks = sorted(sstock.get_list_stocks())
    for stock in lstocks:
        print(stock)
        sorders = StockOrders()
        ldelete = []
        lexecutionsS = []
        lexecutionsB = []

        rfile = open(datapath + 'Messages/' + day + '-' + stock + '-MESSAGES.csv', 'r')
        for mess in rfile:
            data = mess.split(',')
            timestamp = ITCHtime(int(data[1].strip()))
            order = data[2].strip()
            ORN = data[3].strip()
            if order in ['F', 'A']:
                if order == 'A':
                    price = float(data[7].strip())
                else:
                    price = float(data[8].strip())
                sorders.insert_order(stock, order, ORN, otime=timestamp, bos=data[5].strip(), price=price, size=int(data[6].strip()))
            if order == 'U':
                nORN =  data[4].strip()
                sorders.insert_order(stock, order, nORN, timestamp, updid=ORN, price=float(data[6].strip()), size=int(data[5].strip()))
            # Computes the time between placing and order and canceling it
            if order == 'D':
                trans = sorders.query_id(ORN)
                ldelete.append(timestamp.itime - trans[1])
                sorders.insert_order(stock, order, ORN)
            if order in ['E', 'C']:
                trans = sorders.query_id(ORN)
                if trans[2] == 'S':
                    lexecutionsS.append(timestamp.itime - trans[1])

                else:
                    lexecutionsB.append(timestamp.itime - trans[1])

        # Working with the logs
        # Computing a histogram using powers of 10 as discretization of time

        # Deletions
        deletions = np.log10(ldelete)
        hdeletions = np.zeros(mxhval)
        for v in deletions:
            hdeletions[int(v)] += 1

        # normalizing to be able to compare
        hdeletions /= np.sum(hdeletions)
        dhistoD[stock] = hdeletions

        # Sells
        execS =  np.log10(lexecutionsS)
        hsell = np.zeros(mxhval)
        for v in execS:
            hsell[int(v)] += 1

        # normalizing to be able to compare
        hsell /= np.sum(hsell)
        dhistoS[stock] = hsell

        # Buys
        execB =  np.log10(lexecutionsB)
        hbuy = np.zeros(mxhval)
        for v in execB:
            hbuy[int(v)] += 1

        # normalizing to be able to compare
        hbuy /= np.sum(hbuy)
        dhistoB[stock] = hbuy

    tmdist = np.zeros((len(lstocks), len(lstocks)))
    mdist = np.zeros((len(lstocks), len(lstocks)))
    for i, h1 in enumerate(lstocks):
        for j, h2 in enumerate(lstocks):
            mdist[i,j] = hellinger_distance(dhistoD[h1], dhistoD[h2])
    tmdist += mdist

    #mds = MDS(n_components=3, dissimilarity='precomputed', n_jobs=-1)
    mds = SpectralEmbedding(n_components=3, affinity='precomputed', n_jobs=-1)
    data = mds.fit_transform(1-mdist)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.scatter(data[:,0],data[:,1],zs=data[:,2], c='r', depthshade=False,s=100)
    plt.show()
    plt.close()

    mdist = np.zeros((len(lstocks), len(lstocks)))
    for i, h1 in enumerate(lstocks):
        for j, h2 in enumerate(lstocks):
            mdist[i,j] = hellinger_distance(dhistoS[h1], dhistoS[h2])
    tmdist += mdist

    # mds = MDS(n_components=3, dissimilarity='precomputed', n_jobs=-1)
    mds = SpectralEmbedding(n_components=3, affinity='precomputed', n_jobs=-1)
    data = mds.fit_transform(1-mdist)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.scatter(data[:,0],data[:,1],zs=data[:,2], c='r', depthshade=False,s=100)
    plt.show()
    plt.close()

    mdist = np.zeros((len(lstocks), len(lstocks)))
    for i, h1 in enumerate(lstocks):
        for j, h2 in enumerate(lstocks):
            mdist[i,j] = hellinger_distance(dhistoB[h1], dhistoB[h2])
    tmdist += mdist
    # mds = MDS(n_components=3, dissimilarity='precomputed', n_jobs=-1)
    mds = SpectralEmbedding(n_components=3, affinity='precomputed', n_jobs=-1)
    data = mds.fit_transform(1-mdist)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.scatter(data[:,0],data[:,1],zs=data[:,2], c='r', depthshade=False,s=100)
    plt.show()
    plt.close()

    tmdist /= 3
    mds = SpectralEmbedding(n_components=3, affinity='precomputed', n_jobs=-1)
    data = mds.fit_transform(1-tmdist)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.scatter(data[:,0],data[:,1],zs=data[:,2], c='r', depthshade=False,s=100)
    plt.show()
    plt.close()


