"""
.. module:: OrderOld.py

OrderOld.py
*************

:Description: OrderOld.py

    

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
    summary = None
    # status = None

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
            self.oid = data[4].strip()  # id of the order to replace
            self.size = int(data[5].strip())
            self.price = float(data[6].strip())

        if self.type in ['X', 'E', 'C']:
            self.size = int(data[4])

        if self.type == 'C':
            self.price = float(data[6].strip())

        if self.type in ['A', 'F', 'U']:
            self.osize = self.size
            self.history=[self]
            
        if self.type in ['P']:
            self.osize = int(data[6].strip())

    def to_string(self, mode='order'):
        """
        returns a string representing an order

        order - The basic info of an order
        exec - The order after the execution process including its history
        cancel - The order after the cancelation including its history
        :return:
        """
        s = f'{nanoseconds_to_time(self.otime)} ID: {self.id} O: {self.type} S: {self.stock}'
        if self.type in ['A', 'F', 'U']:
            s += f' B/S: {self.buy_sell} SZ: {self.size} PR: {self.price} OSZ: {self.osize}'

        if self.type in ['U']:
            s += f' OID: {self.oid}'

        if self.type in ['E']:
            s += f' SX: {self.size}'

        if self.type in ['C']:
            s += f' SX: {self.size} PR: {self.price}'

        if self.type in ['X']:
            s += f' SX: {self.size}'

        if mode == 'exec':
            s= f'{s}{self.history_to_string()}'
            # s = 'H: ' + self.history[-1][0] + ' ' + str(self.history[-1][1]) + ' <- ' + s
            # s = nanoseconds_to_time(self.history[-1][2]) + ' <- ' + s

        if mode == 'cancel':
            s= f'{s}{self.history_to_string()}'
            # s = 'H: ' + self.history[-1][0] + ' ' + str(self.history[-1][1]) + ' <- ' + s
            # s = nanoseconds_to_time(self.history[-1][2]) + ' <- ' + s


        return s


    def history_to_string(self, last=True):
        """

        Generates a string representing the recorded history of an order
        :return:
        """
        s = ''
        if last:
            if self.type in ['A', 'F', 'U']:
                lasttype = self.history[-1].type  # Type of the last order applied to the order
                delta = self.history[-1].otime - self.otime
                if delta < 1_000_000:
                    dt = 'VHF'
                elif delta < 1_000_000_000:
                    dt = 'HF'
                else:
                    dt = 'N'

                if lasttype == 'C':
                    #s += f'X DeltaT: {nanoseconds_to_time(delta)} -> {self.history[-1].to_string()}'
                    h = f'HIST ----- {dt} D: {nanoseconds_to_time(delta)}\n'
                    for o in self.history:
                        h += f'D= {nanoseconds_to_time(o.otime - self.history[0].otime)}| {o.to_string()}\n'
                    s += f'\n{h}'
                if lasttype == 'E':
                    h = f'HIST ----- {dt} D: {nanoseconds_to_time(delta)}\n'
                    for o in self.history:
                        h += f'D= {nanoseconds_to_time(o.otime - self.history[0].otime)}| {o.to_string()}\n'
                    s += f'\n{h}'

                if lasttype == 'X':
                    s += f'X DeltaT: {nanoseconds_to_time(delta)} -> {self.history[-1].to_string()}'

                if lasttype == 'D':
                    s += f'X DeltaT: {nanoseconds_to_time(delta)} -> {self.history[-1].to_string()}'

                if lasttype == 'U':
                    s += f'X DeltaT: {nanoseconds_to_time(delta)} -> {self.history[-1].to_string()}'


        return s

    def history_time_length(self):
        """
        Returns when there is a history in the order the difference of time between the creation of the order
        and the last transaction in the history (if there is only the transaction then the delta is 0)

        If no history
        :return:
        """

        if self.type in ['A', 'F', 'U']:
            return self.history[-1].otime - self.history[0].otime
        else:
            return None

    def __lt__(self, a):
        """
        less than
        :param a:
        :param b:
        :return:
        """
        return self.price < a.price or (self.price == a.price and self.otime < a.otime)
