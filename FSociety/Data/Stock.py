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

    sstock = None

    def __init__(self, fast=False):
        """

        """

        if fast:
            file = datapath + '/Data/stockfast.csv'
        else:
            file = datapath + '/Data/stockselected.csv'

        rfile = open(file, 'r')
        self.sstocks = {}
        for stock in rfile:
            self.sstocks[stock.strip()] = ''
        rfile.close()

    def get_list_stocks(self):
        """

        :return:
        """
        return sorted(self.sstocks.keys())
