"""
.. module:: ITCHMessages

ITCHMessages
*************

:Description: ITCHMessages

    

:Authors: bejar
    

:Version: 

:Created on: 14/11/2017 17:26 

"""

from FSociety.Config import datapath, ITCH_days
from FSociety.Data.Order import Order
import gzip

__author__ = 'bejar'

class ITCHMessages:
    """
    Streams the orders from a csv MESSAGES file processed from an ITCH file
    """

    path = ''
    year = ''
    day = 0
    stock = ''
    stream = None

    def __init__(self, year='2017G', day=0, stock='AAPL'):
        """
        Initializes the stream

        :param year:
        :param day:
        :param stock:
        """

        self.path = datapath
        if 'G' in year:
            self.path += '/GIS/'
        self.year = year
        self.day = day
        self.stock = stock


    def open(self):
        """
        Opens the stream
        :return:
        """
        self.stream = gzip.open(self.path + 'Messages/' + ITCH_days[self.year][self.day] + '-' + self.stock + '-MESSAGES.csv.gz', 'rt')
        # self.stream = gzip.open(self.path + 'Messages/' + self.day + '-' + self.stock + '-MESSAGES.csv.gz', 'rt')

    def get_order(self):
        """
        Returns an order from the stream
        :return:
        """
        for item in self.stream:
            # print(item)
            yield Order(item)