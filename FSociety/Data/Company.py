"""
.. module:: Companies

Companies
*************

:Description: Companies

    

:Authors: bejar
    

:Version: 

:Created on: 06/09/2016 11:55 

"""

from FSociety.Config import datapath

__author__ = 'bejar'


class Company:

    cnames = {}

    def __init__(self):
        """
        Reads the companies from a file and stores it in a dictionary
        """


        f = open(datapath + '/Data/companylist.csv', 'r')


        for line in f:
            reg = line.split(',')
            if reg[0] != 'Symbol':
                if reg[0] not in self.cnames:
                    self.cnames[reg[0]] = [reg[1], reg[2], reg[3], reg[4].strip()]
                else:
                    if reg[4].strip() != 'ASX':
                        self.cnames[reg[0]] = [reg[1], reg[2], reg[3], reg[4].strip()]


    def get_company(self, cmp):
        """
        Returns the data for the company
        :param cmp:
        :return:
        """
        if cmp in self.cnames:
            return self.cnames[cmp]
        else:
            return None

if __name__ == '__main__':
    c = Company()

    for cmp in sorted(c.cnames.items()):
        print(cmp[0])