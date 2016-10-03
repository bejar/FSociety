"""
.. module:: StockOrders

StockOrders
*************

:Description: StockOrders

    

:Authors: bejar
    

:Version: 

:Created on: 26/09/2016 10:28 

"""

__author__ = 'bejar'
# TODO: This structure should be completed to be able to compute the order book
class StockOrders:
    """
    Class to store the identifiers of the orders in the buy/sell/replace/cancel/delete messages

    Indexing by the id because is the information in the modify, cancel, delete and execution orders

    Each element stores the stock tick and the time of the order
    """
    dorders = None
    def __init__(self):
        """

        """
        self.dorders = {}

    def insert_order(self, stock, order, id, otime=None, bos=None, updid=None, price=None):
        """
        Inserts an order in the structure

        :param order:
        :param id:
        :return:
        """
        if order in ['A', 'F']:
            self.dorders[id] = (stock, int(otime.stamp()), bos, price)
        if order == 'U':
            self.dorders[id] = (stock, int(otime.stamp()), self.dorders[updid][2], price)
        if order == 'D' and id in self.dorders:
            del self.dorders[id]

    def query_id(self, id):
        if id in self.dorders:
            return self.dorders[id]
        else:
            return None




