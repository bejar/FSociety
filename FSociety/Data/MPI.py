"""
.. module:: MPIname

MPIname
*************

:Description: MPIname

    

:Authors: bejar
    

:Version: 

:Created on: 18/07/2016 12:48 

"""
from FSociety.Config import datapath

__author__ = 'bejar'


class MPI():
    """
    Structure for the MPI names
    """
    def __init__(self):
        """
        Reads the MPI names from a file and stores it in a dictionary
        """
        dnames = None

        f = open(datapath + '/Data/mpidlist.txt','r')

        for line in f:
            reg = line.split('|')
            if reg[0]!='MPID':
                if reg[0] not in dnames:
                    dnames[reg[0]] = reg[2]



