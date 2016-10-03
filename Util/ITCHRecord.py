"""
.. module:: ITCHRecord

ITCHRecord
*************

:Description: ITCHRecord

    

:Authors: bejar
    

:Version: 

:Created on: 26/09/2016 8:12 

"""
from Util.ITCHtime import ITCHtime

__author__ = 'bejar'


class ITCHRecord():
    """
    Stores The information of an ITCH record from an ITCH decoded message
    """

    action = None
    timestamp = None
    ORN = None
    nORN = None # for replace orders
    stock = None
    order = None
    shares = None
    price = None
    attribution = None
    opshares = None
    matchnum = None

    def __init__(self, record):
        """

        :param data:
        """
        self.action = self.ext_string(record[0])
        self.timestamp = ITCHtime(record[3])
        if self.action in ['A', 'F', 'E', 'C', 'X', 'D', 'U', 'P']:
            self.ORN = int(record[4])

        if self.action in ['U']:
            self.nORN = int(record[5])

        if self.action in ['A', 'F', 'P']:
            self.stock = self.ext_string(record[7]).strip()
            self.price = int(record[8])

        if self.action in ['A', 'F', 'P']:
            self.order = self.ext_string(record[5])

        if self.action in ['A', 'F', 'U', 'P']:
            self.shares = int(record[6])

        if self.action in ['U']:
            self.price = int(record[7])

        if self.action in ['F']:
            self.attribution = self.ext_string(record[9])

        if self.action in ['E', 'C', 'X']:
            self.opshares = int(record[5])

        if self.action in ['E', 'C']:
            self.matchnum = int(record[6])

        if self.action in ['P']:
            self.matchnum = int(record[9])

        if self.action in ['C', 'P']:
            self.price = int(record[8])



    @staticmethod
    def ext_string(b):
        '''Try to decode b to ascii

        This is why people don't like Python 3
        '''
        try:
            return b.decode('ascii')
        except AttributeError:
            print('Attribute Error')
            return str(b)

    def to_string(self):
        """
        Returns a string with all the information of the record
        :return:
        """
        rstr = ""

        rstr += self.timestamp.stamp()
        rstr += ', ' + self.action

        if self.action in ['A', 'F', 'E', 'C', 'D', 'U', 'P', 'X']:
            rstr += ', ' + str(self.ORN)

        if self.action in ['U']:
            rstr += ', ' + str(self.nORN)

        if self.action in ['A', 'F', 'P']:
            rstr += ', ' + self.stock
            rstr += ', ' + self.order

        if self.action in ['A', 'F', 'U', 'P']:
            rstr += ', ' + str(self.shares)

        if self.action in ['F']:
            rstr += ', ' + self.attribution.strip()

        if self.action in ['E', 'C', 'X']:
            rstr += ', ' + str(self.opshares)

        if self.action in ['E', 'C']:
            rstr += ', ' + str(self.matchnum)

        if self.action in ['A', 'F', 'C', 'U', 'P']:
            rstr += ', ' + str(self.price / 10000)
        return rstr
