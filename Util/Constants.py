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

ITCH_files = ['03302016.NASDAQ_ITCH50.gz', '05272016.NASDAQ_ITCH50.gz',
              '07292016.NASDAQ_ITCH50.gz', '08302016.NASDAQ_ITCH50.gz', '12302016.NASDAQ_ITCH50.gz']
ITCH_days = {'2014': ['06022014', '09022014', '10022014', '11022014', '12022014', '12312014'],
             '2015': ['02022015', '04022015', '05012015', '07302015', '08122015', '10302015', '12302015'],
             '2016': ['03302016', '05272016', '07292016', '08302016', '12302016']}

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

