"""
.. module:: ITCHtime

ITCHtime
*************

:Description: ITCHtime

    

:Authors: bejar
    

:Version: 

:Created on: 18/07/2016 9:20 

"""

__author__ = 'bejar'


class ITCHtime:
    """
    Class for the ITCH time (nanoseconds from midnight)
    """

    itime = 0

    def __init__(self, nnstime):
        """

        """
        self.itime = nnstime
        self.nnseconds = nnstime % 1000
        nnstime //= 1000
        self.mcseconds = nnstime % 1000
        nnstime //= 1000
        self.mlseconds = nnstime % 1000
        nnstime //= 1000
        self.hours = nnstime // 3600
        rhours = nnstime % 3600
        self.minutes = rhours // 60
        self.seconds = rhours % 60

    def to_string(self):
        """
        String representation as HH:MM:SS.mmm.mmm.nnn
        :return:
        """
        return '{:02d}:{:02d}:{:02d}.{:03d}.{:03d}.{:03d}'.format(self.hours, self.minutes, self.seconds,
                                                                  self.mlseconds, self.mcseconds, self.nnseconds)

    def stamp(self):
        """
        Nanoseconds as a string
        :return:
        """
        return str(self.itime)



if __name__ == '__main__':
    itime = ITCHtime(72000083249598)
    print(itime.to_string())