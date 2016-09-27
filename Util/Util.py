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

def now():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def nanoseconds_to_time(nnstime):
    """
    Transforms nanoseconds to readable time
    :param nano:
    :return:
    """
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
    return '{:02d}:{:02d}:{:02d}.{:03d}.{:03d}.{:03d}'.format(hours, minutes, seconds,
                                                                  mlseconds, mcseconds, nnseconds)