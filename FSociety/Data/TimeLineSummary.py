"""
.. module:: TimeLineSummary

TimeLineSummary
*************

:Description: TimeLineSummary

    Given a history of executed/canceled transactions computes information of previous activity

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
from collections import Counter

__author__ = 'bejar'

if __name__ == '__main__':

    year = '2017G'
    day = 0
    stock = 'GOOGL'
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
       lorders.append((o.otime, 'XI', o.id))
       lorders.append((o.history[-1].otime, 'XF', o.id))

    # Add to the list a cancelled order with the time of the initial order and the time of the final cancellation
    for o in lcancelled:
        lorders.append((o.otime, 'CI', o.id))
        lorders.append((o.history[-1].otime, 'CF', o.id))

    lorders = sorted(lorders)

    print(len(lorders))

    # Processes all the itervals for the orders and registers for all the executions a
    # copy of the state of the orders
    #sopen = []
    #scancel = []
    #sexec = []
    cbuy = Counter()
    csell = Counter()
    for t,op,id in lorders:
        if op == 'O':
            if sorders.orders[id].buy_sell == 'B':
                cbuy.update([sorders.orders[id].price])
            else:
                csell.update([sorders.orders[id].price])
            #sopen.append(id)
        elif op == 'CI':
            if sorders.cancelled[id].buy_sell == 'B':
                cbuy.update([sorders.cancelled[id].price])
            else:
                csell.update([sorders.cancelled[id].price])
            #scancel.append(id)
        elif op == 'CF':
            if sorders.cancelled[id].buy_sell == 'B':
                cbuy.subtract([sorders.cancelled[id].price])
            else:
                csell.subtract([sorders.cancelled[id].price])
            #scancel.remove(id)
        elif op == 'XI':
            if sorders.executed[id].buy_sell == 'B':
                cbuy.update([sorders.executed[id].price])
            else:
                csell.update([sorders.executed[id].price])
            #sexec.append(id)
        else:  # it is an execution
            #sorders.executed[id].summary=[sopen[:], scancel[:], sexec[:]]
            #print(f'ID: {id} O: {len(sopen)} C: {len(scancel)} X: {len(sexec)}')
            #input("ready? ")
            if 10000<sorders.executed[id].history_time_length()<100000:
                print('********************************************')
                print(f'ID: {id}')
                print(sorders.executed[id].to_string(mode='exec'))
                if sorders.executed[id].buy_sell == 'B':
                    print(f'BUY: {sorders.executed[id].price}')
                    print(sorted([v for v in cbuy.items() if v[1]>0],reverse=True)[:10])
                else:
                    print(f'SELL: {sorders.executed[id].price}')
                    print(sorted([v for v in csell.items() if v[1]>0])[:10])
                if sorders.executed[id].buy_sell == 'B':
                    cbuy.subtract([sorders.executed[id].price])
                else:
                    csell.subtract([sorders.executed[id].price])
                


#    for o in sorders.executed:
#        print(f'OP: {len(sorders.executed[o].summary[0])} CA: {len(sorders.executed[o].summary[1])}')







