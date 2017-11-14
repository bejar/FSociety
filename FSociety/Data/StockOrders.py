"""
.. module:: StockOrders

StockOrders
*************

:Description: StockOrders

    

:Authors: bejar
    

:Version: 

:Created on: 26/09/2016 10:28 

"""

from FSociety.Data.Order import Order

__author__ = 'bejar'
# TODO: This structure should be completed to be able to compute the order book
class StockOrders:
    """
    Class to store the identifiers of the orders in the buy/sell/replace/cancel/delete messages

    Indexing by the id because is the information in the modify, cancel, delete and execution orders

    Each element stores the stock tick and the time of the order
    """
    orders = None
    def __init__(self):
        """

        """
        self.orders = {}  # Dictionary for active orders
        self.canceled = {}  # Dictionary for canceled orders
        self.executed = {}  # Dictionary for executed orders

    def process_order(self, stock, order, id, otime=None, bos=None, updid=None, price=None, size=None):
        """
        Inserts an order in the structure

        :param stock: Nombre de la accion
        :param otime: Tiempo orden en ITCHtime
        :param bos:  Compra o venta (B/S)
        :param updid: Actualizacion del ID de la orden (para modificaciones)
        :param price: precio de la orden
        :param size: Tamanyo de la orden
        :param order: Tipo de orden
        :param id: Identificador de la orden
        :return:
        """

        # Order Add (B/S)
        if order in ['A', 'F']:
            self.orders[id] = Order(order, id, otime, stock=stock, b_s=bos, price=price, size=size)

        # Order Executed (total or partial)
        if order in ['E']:
            # Modify the size of the order
            self.orders[id].size -= size
            # Add to the history of executions of the order its execution
            self.orders[id].history.append(('E', otime, size))
            # If no shares left, move it to executed
            if self.orders[id].size == 0:
                self.executed[id] = self.orders.pop(id)

        # Order Executed (total or partial) with price
        if order in ['C']:
            if id in self.orders:
                # Modify the size of the order
                self.orders[id].size -= size
                # Add to the history of executions of the order its execution
                self.orders[id].history.append(('C', otime, size, price))
                # If no shares left, move it to executed
                if self.orders[id].size == 0:
                    self.executed[id] = self.orders.pop(id)
            else:
                print('Order vanished')


        # Order Replace (cancel+replace)
        if order == 'U':
            # Add a new order with the new parameters
            self.orders[id] = Order(order, id, otime, stock=stock, b_s=self.orders[updid].buy_sell, price=price, size=size)
            # Delete the original order from active orders
            ro = self.orders.pop(updid)
            # Add the history of the original order
            self.orders[id].history = ro.history + self.orders[id].history

        # Delete Order
        if order == 'D' and id in self.orders:
            self.canceled[id] = self.orders.pop(id)
            self.canceled[id].history.append(('D', otime))

        # Partial cancelation
        if order == 'X' and id in self.orders:
            self.orders[id].size -= size  # Modify the size of the order
            self.orders[id].history.append(('X', otime, size))

    def query_id(self, id):
        if id in self.orders:
            return self.orders[id]
        else:
            return None


    def list_executed(self, mode='order'):
        """
        print executed orders
        :return:
        """
        ltimes = []

        for id in self.executed:
            ltimes.append((self.executed[id].otime, id))

        for _, id in sorted(ltimes):
            print(self.executed[id].to_string(mode=mode))

