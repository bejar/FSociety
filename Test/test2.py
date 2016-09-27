"""
.. module:: test2

test2
*************

:Description: test2

    

:Authors: bejar
    

:Version: 

:Created on: 26/09/2016 10:03 

"""
import operator

__author__ = 'bejar'

file = '../Data/extstocks.csv'


wfile = open(file, 'r')

dstocks = {}

for line in wfile:
    stock, nmess = line.split(',')

    if stock not in dstocks:
        dstocks[stock] = (int(nmess.strip()), 1)
    else:
        dstocks[stock] = (int(nmess.strip()) + dstocks[stock][0], dstocks[stock][1] + 1)

lstocks = []
for stock, vals in dstocks.items():
    lstocks.append((stock, vals[0]))



lstocks = sorted(lstocks, key=operator.itemgetter(1), reverse=True)
for i, stock in enumerate(lstocks):
        print(stock[0])




