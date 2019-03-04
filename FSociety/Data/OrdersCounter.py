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

import seaborn as sn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from FSociety.Util import now, nanoseconds_to_time
import numpy as np
__author__ = 'bejar'


class OrdersCounter:

    countertime = None
    countervalue = None
    countertick = None
    counter = None
    order_types = ('A', 'F', 'E', 'U', 'C', 'D', 'X')
    selected = None
    precision = 3
    granularities = {'mcs': (1000, 5), 'ms': (1000000, 4), 's': (1000000000, 3), 'm': (60000000000, 2)}
    granularity = 1000000000

    def __init__(self, select=None, granularity='s'):
        """
        Initializes the structure of deques for all the order types in deque
        granularity of the counting in nanoseconds

        :param select:
        """

        if granularity not in self.granularities:
                    raise NameError('%s Not a valid granularity [mcs, ms, s, m]' % granularity)

        self.granularity = self.granularities[granularity][0]
        self.precision = self.granularities[granularity][1]

        if select is not None and select is not []:
            for s in select:
                if s not in self.order_types:
                    raise NameError('%s Not a valid order type' % s)
            self.selected = select
        else:
            self.selected = self.order_types

        for s in self.selected:
            self.countertime[s] = []
            self.countervalue[s] = []
            self.countertick[s] = []
            self.counter[s] = [0,0]
        self.countertime['Z'] = []
        self.countervalue['Z'] = []
        self.countertick['Z'] = []
        self.counter['Z'] = [0,0]

        print(self.selected)

    def process_order(self, order):
        """
        Updates the counter
        :param order:
        :return:
        """
        if order.type in self.selected:
            if self.counter[order.type][0] == int(order.otime/self.granularity):
                self.counter[order.type][1] += 1
            else:
                self.countertime[order.type].append(self.counter[order.type][0])
                self.countervalue[order.type].append(self.counter[order.type][1])
                self.countertick[order.type].append(nanoseconds_to_time(self.counter[order.type][0]*self.granularity, prec=self.precision))
                self.counter[order.type] = [int(order.otime/self.granularity), 1]


        if self.counter['Z'][0] == int(order.otime/self.granularity):
            self.counter['Z'][1] += 1
        else:
            self.countertime['Z'].append(self.counter['Z'][0])
            self.countervalue['Z'].append(self.counter['Z'][1])
            self.countertick['Z'].append(nanoseconds_to_time(self.counter['Z'][0]*self.granularity, prec=self.precision))
            self.counter['Z'] = [int(order.otime/self.granularity), 1]

    def plot_counter(self, otype):
        """
        Plots the
        :param otype:
        :return:
        """
        if type(otype) != list:
            otype = [otype]

        fig = plt.figure(figsize=(12,8))
        for i, t in enumerate(otype):
            ax = fig.add_subplot(len(otype), 1, i+1)
            plt.plot(self.countertime[t][1:], self.countervalue[t][1:])
            space = int(np.log2(len(self.countertime[t])))*10
            plt.xticks(self.countertime[t][1::space], self.countertick[t][1::space])#, rotation='vertical')
            # ax.set_xticks(ax.get_xticks()[::20])
            # plt.locator_params(nbins=5, axis='x')
            # ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            plt.ylabel(t)


        plt.subplots_adjust(bottom=0.15)
        plt.show()
        plt.close()


