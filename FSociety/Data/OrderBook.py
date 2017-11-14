"""
.. module:: OrderBook

OrderBook
*************

:Description: OrderBook

    

:Authors: bejar
    

:Version: 

:Created on: 14/11/2017 16:44 

"""

from pqdict import pqdict
from FSociety.Data import Order

__author__ = 'bejar'

class OrderBook:
    """
    Class to maintain the order book
    """

    sell = None
    buy = None

    def __init__(self):
        """
        Create the queues
        """

        self.sell = pqdict()
        self.buy = pqdict()


    def insert_order(self, order):
        """

        :param order:
        :return:
        """

        if order.buy_sell == 'B':
            self.buy[order.id] = order



if __name__ == '__main__':
    pass