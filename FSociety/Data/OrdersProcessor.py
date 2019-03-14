"""
.. module:: OrdersProcessor

StockOrders
*************

:Description: OrdersProcessor

    Procesa ordenes y las guarda en un estructuras de datos

:Authors: bejar
    

:Version: 

:Created on: 26/09/2016 10:28 

"""



__author__ = 'bejar'
# TODO: This structure should be completed to be able to compute the order book
class OrdersProcessor:
    """
    Class to store the identifiers of the orders in the buy/sell/replace/cancel/delete messages

    Indexing by the id because is the information in the modify, cancel, delete and execution orders

    Each element stores the stock tick and the time of the order
    """
    orders = None  # Dictionary for active orders
    cancelled = None  # Dictionary for totally cancelled orders
    executed = None  # Dictionary for totally executed orders

    def __init__(self):
        """
        Record information of the orders modifications and saves the
        executed and canceled transactions (it needs lots of memory and only is feasible
        for individual stocks)
        """
        self.orders = {}
        self.cancelled = {}  # Dictionary for cancelled orders
        self.executed = {}  # Dictionary for executed orders

    def insert_order(self, order):
        """
        Processes a new order and modifies the data structure

        :param order:
        :return:
        """

        # Order Add (B/S)
        if order.type in ['A', 'F']:
            self.orders[order.id] = order

        # Order Executed (total or partial)
        if order.type in ['E']:
            # Modify the size of the order
            self.orders[order.id].size -= order.size
            # Add to the history of executions of the order
            self.orders[order.id].history.append(order)
            # If no shares left, move it to executed
            if self.orders[order.id].size == 0:
                self.executed[order.id] = self.orders.pop(order.id)
            elif self.orders[order.id].size < 0:
                print('--------------------> Shares Overexecuted E')

        # Order Executed (total or partial) with price
        if order.type in ['C']:
            # Modify the size of the order
            self.orders[order.id].size -= order.size
            # Add to the history of executions of the order
            self.orders[order.id].history.append(order)
            # If no shares left, move it to executed
            if self.orders[order.id].size == 0:
                self.executed[order.id] = self.orders.pop(order.id)
            elif self.orders[order.id].size < 0:
                print('--------------------> Shares Overexecuted C')

        # Order Replace (cancel+replace)
        if order.type == 'U':
            # Copy from the original data the B/S value
            order.buy_sell = self.orders[order.oid].buy_sell
            # Add a new order with the new parameters
            self.orders[order.id] = order
            # Delete the original order from active orders
            ro = self.orders.pop(order.oid)
            ro.history.append(order)  # Adds this cancel/replace as the end of original order
            # Move it to cancelled orders
            self.cancelled[order.oid] = ro

        # Delete Order
        if order.type == 'D':
            self.cancelled[order.id] = self.orders.pop(order.id)
            self.cancelled[order.id].history.append(order)

        # Partial cancelation
        if order.type == 'X':
            self.orders[order.id].size -= order.size  # Modify the size of the order
            self.orders[order.id].history.append(order)
            # If there are no shares left move it to cancelled
            if self.orders[order.id].size == 0:
                self.cancelled[order.id] = self.orders.pop(order.id)
            elif self.orders[order.id].size < 0:
               print('--------------------> Shares Overcancelled')


    def query_id(self, id):
        if id in self.orders:
            return self.orders[id]
        elif (self.cancelled is not None) and (id in self.cancelled):
            return self.cancelled[id]
        elif (self.executed is not None) and (id in self.executed):
            return self.executed[id]
        else:
            return None

    def list_executed(self, mode='order', hft=False):
        """
        print executed orders
        :return:
        """
        ltimes = []

        for id in self.executed:
            ltimes.append((self.executed[id].otime, id))

        t = 0
        fdict = {1_000:0,10_000:0,100_000:0,1_000_000:0,10_000_000:0,100_000_000:0,1_000_000_000:0}
        for _, id in sorted(ltimes):
            if hft:
                delta = self.executed[id].history_time_length()
                if delta is not None and 0< delta < 1_000_000_000:
                    print(self.executed[id].to_string(history=mode))
                    for v in fdict:
                        if delta//v == 0:
                            fdict[v]+=1
                            break
                    t += 1
            else:
                print(self.executed[id].to_string(history=mode))
                t+=1

        if hft:
            print(f"{t} HFT transactions ")
            for v in fdict:
                print(f"{v}< {fdict[v]}")
        else:
            print(f"{t} transactions ")



    def list_cancelled(self, mode='order'):
        """
        print cancelled orders
        :return:
        """
        ltimes = []

        for id in self.cancelled:
            ltimes.append((self.cancelled[id].otime, id))

        for _, id in sorted(ltimes):
            print(self.cancelled[id].to_string(history=mode))


    def list_pending_orders(self, mode='order'):
        """
        List orders that are not executed or cancelled
        :return:
        """

        ltimes = []

        for id in self.orders:
            ltimes.append((self.orders[id].otime, id))

        for _, id in sorted(ltimes):
            print(self.orders[id].to_string(history=mode))
            if self.orders[id].history:
                if len(self.orders[id].history)>1:
                    print(self.orders[id].history_to_string())

    def sorted_orders(self, otype='open'):
        """
        Returns a time ordered list with the "open" orders, "executed" orders and "cancelled" orders
        :param type:
        :return:
        """
        if otype == 'open':
            ltimes =[(self.orders[o].otime, self.orders[o]) for o in self.orders]
        elif otype == 'executed':
             ltimes =[(self.executed[o].otime, self.executed[o]) for o in self.executed]
        elif otype == 'cancelled':
             ltimes =[(self.cancelled[o].otime, self.cancelled[o]) for o in self.cancelled]
        else:
            ltimes = []

        return([o for _, o in sorted(ltimes)])


if __name__ == '__main__':
    from FSociety.ITCH import ITCHMessages

    year = '2017G'
    day = 0
    stock = 'MSFT'
    rfile = ITCHMessages(year, day, stock)
    rfile.open()
    sorders = OrdersProcessor()
    for order in rfile.get_order():
        # print(order.to_string(history=False))
        sorders.insert_order(order)


    #sorders.list_pending_orders()

    for o in sorders.sorted_orders(otype='cancelled'):
        print(o.to_string(history=True))




