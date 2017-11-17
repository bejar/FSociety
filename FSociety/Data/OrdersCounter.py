"""
.. module:: OrdersCounter

OrdersCounter
*************

:Description: OrdersCounter

    Generates counting statistics for the orders stream

:Authors: bejar
    

:Version: 

:Created on: 17/11/2017 11:31 

"""

from collections import deque

__author__ = 'bejar'


class OrdersCounter:

    counter = {}
    order_types = ('A', 'F', 'E', 'U', 'C', 'D', 'X')
    selected = []
    granularity = 1000
    statistic = {}

    def __init__(self, select=None, granularity=1000):
        """
        Initializes the structure of deques for all the order types in deque
        granularity of the counting in nanoseconds

        :param select:
        """

        self.granularity = granularity
        if select is not None and select is not []:
            for s in select:
                if s not in self.order_types:
                    raise NameError('%s Not a valid order type' % s)
            self.selected = select
        else:
            self.selected = self.order_types

        for s in self.selected:
            self.counter[s] = deque()
            self.statistic[s] = []


    def process_order(self, order):
        """
        Updates the counter
        :param order:
        :return:
        """
        pass
        # if counter







