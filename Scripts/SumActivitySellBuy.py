"""
.. module:: SumActivitySellBuy

SumActivitySellBuy
*************

:Description: SumActivitySellBuy

    

:Authors: bejar
    

:Version: 

:Created on: 10/11/2017 10:54 

"""

import argparse
from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime
from FSociety.Util import now
from FSociety.Data import Company
from FSociety.Config import datapath, ITCH_days
import pandas as pd

__author__ = 'bejar'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default=None)

    args = parser.parse_args()

    year = args.year

    if year is None:
        year = '2017G'

    if 'G' in year:
        lfiles = [day + '-STOCK-ACTIVITY.csv.gz' for day in ITCH_days[year]]
        datapath = datapath + '/GIS/Results/'


    ldf = []
    for file in lfiles[:-1]:
        ldf.append(pd.read_csv(datapath + file, header=None, index_col=0, names=['Name', 'Buy', 'Sell'], usecols=[0, 1,2]))

    idf = ldf[0]
    for df in ldf[1:]:
        idf = idf.add(df, fill_value=0)

    idf['Nops'] = idf['Buy'] + idf['Sell']
    print(idf.head())

    idf.sort_values('Nops', ascending=False, inplace=True)
    print(idf.head())
    for id in idf.index:
        print(id)

