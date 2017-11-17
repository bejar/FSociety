"""
.. module:: Util

Util
*************

:Description: Util

    

:Authors: bejar
    

:Version: 

:Created on: 18/07/2016 14:26 

"""

__author__ = 'bejar'

import time
import numpy as np

def now():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def nanoseconds_to_time(nnstime, prec=6):
    """
    Transforms nanoseconds to readable time
    :param nano:
    :return:
    """
    lfmt = ['{:02d}', ':{:02d}', ':{:02d}', '.{:03d}', '.{:03d}', '.{:03d}']
    nnstime = int(nnstime)
    nnseconds = nnstime % 1000
    nnstime //= 1000
    mcseconds = nnstime % 1000
    nnstime //= 1000
    mlseconds = nnstime % 1000
    nnstime //= 1000
    hours = nnstime // 3600
    rhours = nnstime % 3600
    minutes = rhours // 60
    seconds = rhours % 60
    ltimes = [hours, minutes, seconds, mlseconds, mcseconds, nnseconds]
    s = ''
    for i in range(prec):
        s += lfmt[i].format(ltimes[i])
    return s

def time_to_nanoseconds(hour, minute=0):
    """
    Computes the nanoseconds for hour:minute
    :param hour: 
    :param minute: 
    :return: 
    """

    return (hour * 60 + minute) * 60 * 1000 * 1000 * 1000

def capped_prices(lprices):
    """
    List of prices without extreme values
    :param lprices:
    :return:
    """
    price_std = np.std(lprices)
    price_mean = np.mean(lprices)
    aprice = np.array(lprices)
    aprice = aprice[np.logical_and(aprice > (price_mean - (price_std)),
                                aprice < (price_mean + (price_std)))]

    return aprice

def hellinger_distance(m1, m2):
    """
    Bhattacharyya distance between two probability matrices/vectors
    :param m1:
    :param m2:
    :return:
    """
    sum = 0.0
    for a, b in zip(m1, m2):
        sum += np.sum((np.sqrt(a) - np.sqrt(b)) ** 2)
    return (1/np.sqrt(2)) * np.sqrt(sum)