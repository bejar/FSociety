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

__author__ = 'bejar'


class Stock:

    sstock = None
    def __init__(self, abs=True):
        """

        """
        if abs:
            file = '../Data/stocksel.csv'
        else:
            file = 'Data/stocksel.csv'
        rfile = open(file, 'r')
        self.sstocks = {}
        for stock in rfile:
            self.sstocks[stock.strip()] = ''
        rfile.close()

    def get_list_stocks(self):
        """

        :return:
        """
        return self.sstocks.keys()
