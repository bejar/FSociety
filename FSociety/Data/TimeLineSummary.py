"""
.. module:: TimeLineSummary

TimeLineSummary
*************

:Description: TimeLineSummary

    Given a history of eecuted/canceled transactions computes information of previous activity

     - Active orders (A/F)
     - Prices

:Authors: bejar
    

:Version: 

:Created on: 26/02/2019 8:45 

"""

from FSociety.ITCH import ITCHv5, ITCHRecord, ITCHtime, ITCHMessages
from FSociety.Util import now, nanoseconds_to_time
from FSociety.Data import Stock, OrdersProcessor, Company, OrdersCounter
from FSociety.Config import datapath, ITCH_days


__author__ = 'bejar'

if __name__ == '__main__':

    year = '2017G'
    day = 0
    stock = 'MSFT'
    rfile = ITCHMessages(year, day, stock)
    rfile.open()
    sorders = OrdersProcessor(history=True)
    for order in rfile.get_order():
        # print(order.to_string())
        sorders.insert_order(order)


    #sorders.list_pending_orders()

    lopen = sorders.sorted_orders(otype='open')
    lexecuted = sorders.sorted_orders(otype='executed')
    lcancelled = sorders.sorted_orders(otype='cancelled')

    # list for storing all the orders in chonological order
    lorders = []

    # Add to the list an open order with its time
    for o in lopen:
        lorders.append((o.otime, 'O', o.id))

    # Add to the list an executed order with the time of the last execution
    for o in lexecuted:
        lorders.append((o.history[-1].otime, 'XF', o.id))

    # Add to the list a cancelled order with the time of the initial order and the time of the final cancellation
    for o in lcancelled:
        lorders.append((o.otime, 'CI', o.id))
        lorders.append((o.history[-1].otime, 'CF', o.id))

    lorders = sorted(lorders)

    # Processes all the itervals for the orders and registers for all the executions a
    # copy of the state of the orders
    sopen = []
    scancel = []
    for o in lorders:
        if o[1] == 'O':
            sopen.append(o[2])
        elif o[1] == 'CI':
            scancel.append(o[2])
        elif o[1] == 'CF':
            scancel.remove(o[2])
        else:  # it is an execution
            sorders.executed[o[2]].summary=[sopen[:], scancel[:]]


    for o in sorders.executed:
        print(f'OP: {len(sorders.executed[o].summary[0])} CA: {len(sorders.executed[o].summary[1])}')







