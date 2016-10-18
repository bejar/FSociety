"""
.. module:: Constants

Constants
*************

:Description: Constants

    Constants for the project

:Authors: bejar
    

:Version: 

:Created on: 15/07/2016 13:19 

"""

__author__ = 'bejar'

datapath = '/home/bejar/storage/Data/ITCH/'

ITCH_files = ['12302015.NASDAQ_ITCH50.gz',  '03302016.NASDAQ_ITCH50.gz', '05272016.NASDAQ_ITCH50.gz',
              '07292016.NASDAQ_ITCH50.gz', '08302016.NASDAQ_ITCH50.gz']
ITCH_days = ['12302015', '03302016', '05272016', '07292016', '08302016']

NASDAQ_actions = {
    'S': 'System Event Message',
    'R': 'Stock Directory Message',
    'H': 'Stock Trading Action Message',
    'Y': 'Reg SHO Restriction',
    'L': 'Market Participation Position Message',
    'V': 'MWCB Decline Level Message',
    'W': 'MWCB Breach Message',
    'K': 'IPO Quoting Period Update',
    'A': 'Add Order Message',
    'F': 'Add Order (MPID) Message',
    'E': 'Order Executed Message',
    'C': 'Order Executed (with Price) Message',
    'X': 'Order Cancel Message',
    'D': 'Order Delete Message',
    'U': 'Order Replace Message',
    'P': 'Trade Message',
    'Q': 'Cross Trade Message',
    'B': 'Broken Trade Message',
    'I': 'NOII Message'
}

