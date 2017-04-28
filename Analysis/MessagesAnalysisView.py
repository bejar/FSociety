"""
.. module:: MessagesAnalysisView

MessagesAnalysisView
*************

:Description: MessagesAnalysisView

    Visualizacion para todas las acciones la distribucion de numero de operaciones, ventas/compras y
    tiempos entre ventas/compras y borrados

:Authors: bejar
    

:Version: 

:Created on: 30/09/2016 10:41 

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from FSociety.Util import datapath

__author__ = 'bejar'

if __name__ == '__main__':
    # 5272016 3302016 12302015

    data = pd.read_csv(datapath + '/Results/MessagesStats.csv')

    datas = data[data.Day==3302016]

    ax = sns.distplot(datas.iloc[:,2],  kde=True, hist=False, color='r')
    plt.show()
    plt.close()

    ax = sns.distplot(datas.iloc[:,3],  kde=True, hist=False, color='r')
    ax = sns.distplot(datas.iloc[:,7],  kde=True, hist=False, color='g')
    plt.show()
    plt.close()


    mtimeS = datas.iloc[:,4].copy()
    mtimeB = datas.iloc[:,8].copy()
    mtimeD = datas.iloc[:,12].copy()

    ax = sns.distplot(np.log10(mtimeS),  kde=True, hist=False, color='r')
    ax = sns.distplot(np.log10(mtimeB),  kde=True, hist=False, color='g')
    ax = sns.distplot(np.log10(mtimeD),  kde=True, hist=False, color='k')
    plt.show()
    plt.close()


    mtimeS = datas.iloc[:,6].copy()
    mtimeB = datas.iloc[:,10].copy()
    mtimeD = datas.iloc[:,14].copy()

    ax = sns.distplot(np.log10(mtimeS),  kde=True, hist=False, color='r')
    ax = sns.distplot(np.log10(mtimeB),  kde=True, hist=False, color='g')
    ax = sns.distplot(np.log10(mtimeD),  kde=True, hist=False, color='k')
    plt.show()
    plt.close()

