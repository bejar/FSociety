"""
.. module:: MessagesDailyDetailsView

MessagesDailyDetailsView
*************

:Description: MessagesDailyDetailsView

    

:Authors: bejar
    

:Version: 

:Created on: 13/11/2017 11:42 

"""


from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime
from FSociety.Util import now, nanoseconds_to_time, capped_prices
from FSociety.Data import Stock, StockOrders, Company
from FSociety.Config import datapath, ITCH_days
import pickle
import os.path
import seaborn as sn
import matplotlib.pyplot as plt
import argparse
import gzip
import numpy as np

__author__ = 'bejar'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='')

    args = parser.parse_args()
    year = str(args.year)
    sstocks = Stock()

    if year == '':
        year = '2017G'

    if 'G' in year:
        lfiles = ['/S' + day + '-v50.txt.gz' for day in ITCH_days[year]]
        datapath = datapath + '/GIS/'
    else:
        lfiles = [day + '.NASDAQ_ITCH50.gz' for day in ITCH_days[year]]

    sstock = Stock(num=50)
    cpny = Company()

    for stock in sorted(sstock.get_list_stocks()):
        for day in ITCH_days[year]:
            if os.path.isfile(datapath + '/Results/' + day + '-' + stock + '-MessageAnalysis.pkl'):
                print(day, stock)
                wfile = open(datapath + '/Results/' + day + '-' + stock + '-MessageAnalysis.pkl', 'rb')
                ddata = pickle.load(wfile)
                wfile.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(np.log10(ddata['DeltaTimeExecSell']), kde=True, norm_hist=True)
                plt.title('Log plot of Sell execution delta time ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(capped_prices(ddata['PriceOrderSell']),  kde=True, norm_hist=True)
                plt.title('Orders Sell price ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(np.log10(ddata['DeltaTimeExecBuy']),  kde=True, norm_hist=True)
                plt.title('Log plot of Buy execution time ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(capped_prices(ddata['PriceOrderBuy']),  kde=True, norm_hist=True)
                plt.title('Orders Buy price ' + day)
                plt.show()
                plt.close()


                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(np.log10(ddata['DeltaTimeDelete']), kde=True, norm_hist=True)
                plt.title('Log plot of deletion time ' + day)
                plt.show()
                plt.close()


                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(np.log10(ddata['DeltaTimeExecSell']),  kde=True, hist=False, color='r')
                ax = sn.distplot(np.log10(ddata['DeltaTimeExecBuy']),  kde=True, hist=False, color='g')
                ax = sn.distplot(np.log10(ddata['DeltaTimeDelete']),  kde=True, hist=False, color='k')
                plt.title('Sell/Buy/Deletion time ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(capped_prices(ddata['PriceOrderSell']),  kde=True, hist=False, color='r')
                ax = sn.distplot(capped_prices(ddata['PriceOrderBuy']),  kde=True, hist=False, color='g')
                plt.title('Sell/Buy orders prices distribution ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(ddata['SizeOrderSell'],  kde=True, hist=True, color='r')
                ax = sn.distplot(ddata['SizeOrderBuy'],  kde=True, hist=True, color='g')
                plt.title('Sell/Buy orders sizes distribution ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(ddata['SizeExecSell'],  kde=True, hist=True, color='r')
                ax = sn.distplot(ddata['SizeExecBuy'],  kde=True, hist=True, color='g')
                ax = sn.distplot(ddata['SizeExecHidden'],  kde=True, hist=True, color='k')
                plt.title('Sell/Buy/Hidden execution sizes distribution ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(12,8))
                ax = sn.distplot(capped_prices(ddata['PriceExecSell']),  kde=True, hist=False, color='r')
                ax = sn.distplot(capped_prices(ddata['PriceExecBuy']),  kde=True, hist=False, color='g')
                ax = sn.distplot(capped_prices(ddata['PriceExecHidden']),  kde=True, hist=False, color='k')
                plt.title('Sell/Buy/Hidden execution prices distribution ' + day)
                plt.show()
                plt.close()

                fig = plt.figure(figsize=(14,8))
                plt.plot(ddata['TimeOrderSell'], ddata['PriceOrderSell'], color='r')
                plt.plot(ddata['TimeOrderBuy'], ddata['PriceOrderBuy'], color='g')
                plt.scatter(ddata['TimeExecSell'], ddata['PriceExecSell'],  marker='o', color='y', s=ddata['SizeExecSell'])
                plt.scatter(ddata['TimeExecBuy'], ddata['PriceExecBuy'],  marker='o', color='b', s=ddata['SizeExecBuy'])
                plt.scatter(ddata['TimeExecHidden'], ddata['PriceExecHidden'], marker='o', color='k', s=ddata['SizeExecHidden'])

                plt.title('Order Sell/Buy price evolution ' + day)
                plt.show()
                plt.close()