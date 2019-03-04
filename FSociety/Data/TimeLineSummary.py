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

import argparse
from FSociety.ITCH import ITCHMessages
from FSociety.Data import OrdersProcessor
from FSociety.Config import ITCH_days
from collections import Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from FSociety.Data import Stock

def sum_count(count, lim=0):
    """
    Sums the total of the counter
    :param count:
    :return:
    """
    if lim == 0:
        return np.sum([v for _, v in count])
    else:
        return np.sum([v for _, v in count[:lim]])


__author__ = 'bejar'

timelines = [10_000_000_000, 1_000_000_000, 100_000_000, 10_000_000, 1_000_000, 100_000, 10_000, 0]
ntimelines = ['inf-10s', '10s-1s', '1s-100ms', '100ms-10ms', '10ms-1ms', '1ms-100 mcs', '100mcs-10mcs', '10mcs-0']
stat = ['price', 'gap', 'lenbuy', 'lensell', 'lenbuy5', 'lensell5', 'lenbuy10', 'lensell10', 'otherprice']


def in_timeline(v):
    """
    Computes the timeline of the executed transaction

    :param v:
    :return:
    """
    for i, t in enumerate(timelines):
        if v > t:
            return i


def order_exec_analysis(year, day, stock, logging=False):
    """

    :param year:
    :param day:
    :param stock:
    :return:
    """
    ## Structure for collecting statistics
    statistics = {v: {} for v in timelines}
    for v in statistics:
        statistics[v]['buy'] = {s: [] for s in stat}
        statistics[v]['sell'] = {s: [] for s in stat}


    rfile = ITCHMessages(year, day, stock)
    rfile.open()
    sorders = OrdersProcessor(history=True)
    for order in rfile.get_order():
        sorders.insert_order(order)

    lopen = sorders.sorted_orders(otype='open')
    lexecuted = sorders.sorted_orders(otype='executed')
    lcancelled = sorders.sorted_orders(otype='cancelled')

    # list for storing all the orders in chonological order
    lorders = []

    # Add to the list an open order with its time
    for o in lopen:
        lorders.append((o.otime, 'O', o.id))

    # Add to the list an executed order with the time of all the partial
    # executions and the last execution
    for o in lexecuted:
        lorders.append((o.otime, 'XI', o.id))
        # Partial executions
        for xo in range(1, len(o.history) - 1):
            if o.history[xo].type in ['C', 'E']:
                lorders.append((o.history[xo].otime, f'XF{xo}', o.id))
        # Final execution
        lorders.append((o.history[-1].otime, f'XF', o.id))

    # Add to the list a cancelled order with the time of the initial order
    # all the possible partial executions
    # and the time of the final cancellation
    for o in lcancelled:
        lorders.append((o.otime, 'CI', o.id))
        for xo in range(1, len(o.history) - 1):
            if o.history[xo].type in ['C', 'E']:
                lorders.append((o.history[xo].otime, f'XF{xo}', o.id))
        lorders.append((o.history[-1].otime, 'CF', o.id))

    lorders = sorted(lorders)

    # Processes all the itervals for the orders and registers for all the executions a
    # some statistics
    cbuy = Counter()
    csell = Counter()
    for _, op, orderid in lorders:
        if op == 'O':
            if sorders.orders[orderid].buy_sell == 'B':
                cbuy[sorders.orders[orderid].price] += 1
            else:
                csell[sorders.orders[orderid].price] += 1
            # sopen.append(orderid)
        elif op == 'CI':
            if sorders.cancelled[orderid].buy_sell == 'B':
                cbuy[sorders.cancelled[orderid].price] += 1
            else:
                csell[sorders.cancelled[orderid].price] += 1
            # scancel.append(orderid)
        elif op == 'CF':
            if sorders.cancelled[orderid].buy_sell == 'B':
                cbuy[sorders.cancelled[orderid].price] -= 1
            else:
                csell[sorders.cancelled[orderid].price] -= 1
            # scancel.remove(orderid)
        elif op == 'XI':
            if sorders.executed[orderid].buy_sell == 'B':
                cbuy[sorders.executed[orderid].price] += 1
            else:
                csell[sorders.executed[orderid].price] += 1
            # sexec.append(orderid)
        else:  # it is an execution

            # If is a final execution the code is 'XF', else it has a number attached
            # The final execution eliminates the price from the order book
            if len(op) == 2:
                if sorders.executed[orderid].buy_sell == 'B':
                    cbuy[sorders.executed[orderid].price] -= 1
                else:
                    csell[sorders.executed[orderid].price] -= 1
            pendingbuy = sorted([v for v in cbuy.items() if v[1] > 0], reverse=True)
            pendingsell = sorted([v for v in csell.items() if v[1] > 0])

            if len(pendingbuy) > 0:
                bestbuy = pendingbuy[0][0]
            else:
                bestbuy = -1
                print('cola vacia BUY')
            if len(pendingsell) > 0:
                bestsell = pendingsell[0][0]
            else:
                bestsell = -1
                print('cola vacia SELL')

            if len(op) == 2:
                timeline = in_timeline(sorders.executed[orderid].history_time_length())
            else:
                timeline = in_timeline(sorders.executed[orderid].history_time_length(dist=int(op[2:])))

            # print(f'{sorders.executed[orderid].price} {pendingbuy[0]} {pendingsell[0]}')

            if (timeline >= 0) and (bestsell != -1) and (bestbuy != -1):
                if logging:
                    print(f'******************************************** {op[2:]}')
                    print(f'ID: {orderid}')
                    print(sorders.executed[orderid].to_string(history=True))

                if sorders.executed[orderid].buy_sell == 'B':
                    buy_sell = 'buy'
                    gap = bestsell - sorders.executed[orderid].price
                    diff = sorders.executed[orderid].price - bestbuy
                    if logging:
                        print(f'BUY: {sorders.executed[orderid].price} / GAP: {gap} / DIFF: {diff}')
                        if gap < 0 or diff < 0:
                            print(f'?????????????????????????????????????????????????????????????')
                            print(f'P:{sorders.executed[orderid].price} BS: {bestsell} BB: {bestbuy}')
                else:
                    buy_sell = 'sell'
                    gap = sorders.executed[orderid].price - bestbuy
                    diff = bestsell - sorders.executed[orderid].price
                    if logging:
                        print(f'SELL: {sorders.executed[orderid].price} / GAP: {gap} / DIFF: {diff}')
                        if gap < 0 or diff < 0:
                            print(f'?????????????????????????????????????????????????????????????')
                            print(f'P:{sorders.executed[orderid].price} BS: {bestsell} BB: {bestbuy}')

                if logging:
                    print(f'QSELL5={pendingsell[:5]}')
                    print(f'QBUY5={pendingbuy[:5]}')
                    print(f'BBUY={bestbuy} BSELL={bestsell}')
                    print(f'LQBUY={sum_count(pendingbuy)} LQSELL={sum_count(pendingbuy)}')

                statistics[timelines[timeline]][buy_sell]['price'].append(sorders.executed[orderid].price)
                statistics[timelines[timeline]][buy_sell]['lenbuy'].append(sum_count(pendingbuy))
                statistics[timelines[timeline]][buy_sell]['lensell'].append(sum_count(pendingsell))
                statistics[timelines[timeline]][buy_sell]['lenbuy5'].append(sum_count(pendingbuy, lim=5))
                statistics[timelines[timeline]][buy_sell]['lensell5'].append(sum_count(pendingsell, lim=5))
                statistics[timelines[timeline]][buy_sell]['lenbuy10'].append(sum_count(pendingbuy, lim=10))
                statistics[timelines[timeline]][buy_sell]['lensell10'].append(sum_count(pendingsell, lim=10))
                statistics[timelines[timeline]][buy_sell]['otherprice'].append(diff)
                statistics[timelines[timeline]][buy_sell]['gap'].append(gap)


    for st in stat:
        for v in timelines:
            statistics[v]['buy'][st] = np.array(statistics[v]['buy'][st])
            statistics[v]['sell'][st] = np.array(statistics[v]['sell'][st])

    return statistics


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help="Anyo del analisis", default='2017G')
    parser.add_argument('--day', help="dia del anyo", type=int, default=0)
    parser.add_argument('--stock', help="Stock del analisis", default='GOOGL')
    parser.add_argument('--log', help="Prints order executions", action='store_true', default=False)
    args = parser.parse_args()

    sstocks = Stock(num=50)
    for stock in sstocks.get_list_stocks():
        statistics = order_exec_analysis(args.year, args.day, stock, logging=args.log)

        for st in stat:
            plt.title(f'buy - {st} / DAY: {ITCH_days[args.year][args.day]} STOCK: {stock}')
            for v in timelines[:-1]:
                sns.distplot(statistics[v]['buy'][st], hist=True, norm_hist=True, bins=10,
                             label=ntimelines[timelines.index(v)])
            plt.legend()
            plt.show()

            plt.title(f'sell - {st} / DAY: {ITCH_days[args.year][args.day]} STOCK: {stock}')
            for v in timelines[:-1]:
                sns.distplot(statistics[v]['sell'][st], hist=True, norm_hist=True, bins=10,
                             label=ntimelines[timelines.index(v)])
            plt.legend()
            plt.show()
