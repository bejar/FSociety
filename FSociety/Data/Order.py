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
from FSociety.ITCH import ITCHtime

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

    # def __init__(self, type, id, otime, stock=None, b_s=None,price=0, size=0):
    #     """
    #     Creates an order object
    #
    #     :param type:
    #     :param id:
    #     :param stock:
    #     :param b_s:
    #     :param otime:
    #     :param price:
    #     :param size:
    #     """
    #     self.type = type
    #     self.id = id
    #     self.otime = otime
    #     # self.status = 'A'  # Active (I - executed, C - canceled, D - deleted)
    #
    #     if type in ['A', 'F', 'E', 'U']:
    #         self.stock = stock
    #
    #     if type in ['A', 'F', 'U']:
    #         self.price = price
    #         self.size = size
    #         self.osize = size
    #         self.buy_sell = b_s
    #         self.history = [(type, id, otime, price, size)]

    def __init__(self, mess):
        """
        Creates an order from a line in the MESSAGES csv file

        :param line:
        :return:
        """
        data = mess.split('&')
        self.stock = data[0][1:-1]
        self.otime = ITCHtime(int(data[1].strip())).itime
        self.type = data[2].strip()
        self.id = data[3].strip()

        if self.type in ['F', 'A']:

            self.price = float(data[7].strip())
            if self.type == 'F':
                self.attr = data[8].strip() # MPI attibution
            self.size = int(data[6].strip())
            self.buy_sell = data[5].strip()

        if self.type == 'U':
            self.oid = data[4].strip() # id of the order to replace
            self.size = int(data[5].strip())
            self.price = float(data[6].strip())

        if self.type in ['X', 'E', 'C']:
            self.size = int(data[4])

        if self.type == 'C':
            self.price = float(data[6].strip())

        if type in ['A', 'F', 'U']:
            self.osize = self.size
            self.history = [(type, id, self.otime, self.price, self.size)]

    def to_string(self, mode='order'):
        """
        returns a string representing an order

        order - The basic info of an order
        exec - The order after the excution process including its history

        :return:
        """
        s = nanoseconds_to_time(self.otime) + 'ID: ' + str(self.id) + ' O: ' +self.type + ' S: ' + self.stock
        if self.type in ['A', 'F']:
            s += ' B/S: ' + self.buy_sell + ' SZ: ' + str(self.size) + ' PR: ' + str(self.price)

        if self.type in ['U']:
            s += ' OID: ' + self.oid
        if mode == 'exec':
            s = nanoseconds_to_time(self.history[-1][1]) + ' <- ' + s
        return s

    # def to_string2(self):
    #     s = nanoseconds_to_time(self.otime)
    #     s += 'ID: ' + str(self.id)
    #     s+= ' O: ' + self.type
    #     s+= ' S: ' + self.stock
    #     if self.type in ['A', 'F']:
    #         s += ' B/S: ' + self.buy_sell
    #         s += ' SZ: ' + str(self.size)
    #         s += ' PR: ' + str(self.price)
    #     return s

    def __lt__(self, a):
        """
        less than
        :param a:
        :param b:
        :return:
        """
        return self.price < a.price or (self.price == a.price and self.otime < a.otime)
