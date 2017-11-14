"""
.. module:: Order.py

Order.py
*************

:Description: Order.py

    

:Authors: bejar
    

:Version: 

:Created on: 14/11/2017 8:36 

"""
from FSociety.Util import nanoseconds_to_time

__author__ = 'bejar'


class Order:
    """
    Class for storing order information
    """

    type = None
    id = 0
    stock = None
    buy_sell = None
    otime = 0
    price = 0
    size = 0
    history = []
    # status = None

    def __init__(self, type, id, otime, stock=None, b_s=None,price=0, size=0):
        """
        Creates an order object

        :param type:
        :param id:
        :param stock:
        :param b_s:
        :param otime:
        :param price:
        :param size:
        """
        self.type = type
        self.id = id
        self.otime = otime
        # self.status = 'A'  # Active (I - executed, C - canceled, D - deleted)

        if type in ['A', 'F', 'E', 'U']:
            self.stock = stock

        if type in ['A', 'F', 'U']:
            self.price = price
            self.size = size
            self.osize = size
            self.buy_sell = b_s
            self.history = [(type, id, otime, price, size)]

    def to_string(self, mode='order'):
        """
        returns a string representing an order
        :return:
        """
        s = nanoseconds_to_time(self.otime) + 'ID: ' + str(self.id)+ ' O: ' +self.type + ' S: '+ self.stock
        if self.type in ['A', 'F', 'U']:
            s += ' B/S: ' + self.buy_sell + ' SZ: ' + str(self.osize) + ' PR: ' + str(self.price)
        if mode == 'exec':
            s = nanoseconds_to_time(self.history[-1][1]) + ' <- ' + s
        return s


