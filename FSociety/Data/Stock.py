"""
.. module:: Stock

Stock
*************

:Description: Stock

Class for representing a structure of stocks
    

:Authors: bejar
    

:Version: 

:Created on: 29/09/2016 15:41 

"""

from FSociety.Config import datapath

__author__ = 'bejar'


class Stock:

    sstocks = None

    def __init__(self, fast=False, num=100):
        """

        """

        if fast:
            file = datapath + '/Data/stockfast.csv'
        else:
            file = datapath + '/Data/stockmonth.csv'

        rfile = open(file, 'r')
        self.sstocks = set()
        i = 0
        for stock in rfile:
            self.sstocks.add(stock.strip())
            i += 1
            if i > num-1: break
        rfile.close()

    def get_list_stocks(self):
        """

        :return:
        """
        return sorted(self.sstocks)

if __name__ == '__main__':
    s = Stock(num=50)
    print(s.get_list_stocks())
    print('AAPL' in s.sstocks)
