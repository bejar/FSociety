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

timelines = [10_000_000_000, 1_000_000_000, 100_000_000, 10_000_000, 1_000_000, 100_000, 10_000, 0]
ntimelines = ['inf-10s', '10s-1s', '1s-100ms', '100ms-10ms', '10ms-1ms', '1ms-100 mcs', '100mcs-10mcs', '10mcs-0']
stat = ['price', 'gap', 'lenbuy', 'lensell', 'lenbuy5', 'lensell5', 'lenbuy10', 'lensell10', 'otherprice', 'size']



ITCH_days = {
             '2015': ['02022015', '04022015', '05012015', '07302015', '08122015', '10302015', '12302015'],
             '2016': ['03302016', '05272016', '07292016', '08302016', '12302016'],
             '2017': ['01302017','03302017', '05302017', '07282017', '08302017'],

             '2018G': ['020118', '020218', '020518', '020618', '020718', '020818', '020918', '021218', '021318',
                       '021418', '021518', '021618', '022018', '022118', '022218', '022318', '022618', '022718', '022818'],
             '2017G': ['020117', '020217', '020317', '020617', '020717', '020817', '020917', '021017', '021317',
                       '021417', '021517', '021617', '021717', '022117', '022217', '022317', '022417', '022717', '022817'],
             '2016G': ['010416', '010516', '010616', '010716', '010816', '011116', '011216', '011316', '011416',
                       '011516', '011916', '012016', '012116', '012216', '012516', '012616', '012716', '012816', '012916'],

             '201811G': ['110118', '110218', '110518', '110618', '110718', '110818', '110918', '111218', '111318',
                         '111418', '111518', '111618', '111918', '112018', '112118', '112318', '112618', '112718', '112818',
                         '112918', '113018'
             ],
             '201812G': ['120318', '120418', '120618', '120718', '121018', '121118', '121218', '121318', '121418',
                       '121718', '121818', '121918', '122018', '122118', '122418', '122618', '122718', '122818', '123118'],

             '201901G': ['010219', '010319', '010419', '010719', '010819', '010919', '011019', '011119', '011419',
                         '011519', '011619', '011719', '011819', '012219', '012319', '012419', '012519', '012817', '012919',
                         '013019', '013119'
             ],
}

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

