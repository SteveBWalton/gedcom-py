# -*- coding: utf-8 -*-

'''
Module to support places in the gedcom python library.
This module implements the :py:class:`GedComPlace` class.
'''
# System Libraries.
from enum import Enum



class GedComPlaceAccuracy(Enum):
    KNOWN = 1
    ABOUT = 2
    ESTIMATED = 3
    CALCULATED = 4


class GedComPlace:
    '''
    Class to represent a place in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''


    def __init__(self, gedcomFile = None):
        '''
        Class constructor for the :py:class:`GedComPlace` class.
        '''
        self.parse(gedcomFile)
        #self.status = GedComDateStatus.EMPTY
        #self.isAbout = False
        #self.dayStatus = GedComDateStatus.UNKNOWN
        #self.monthStatus = GedComDateStatus.UNKNOWN
        #self.yearStatus = GedComDateStatus.UNKNOWN
        ## pub is_month_quarter: bool,
        #self.theDate = datetime.date.today()



    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the string.
        '''
        self.place = None
        self.address = None
        self.country = None
        self.latitude = None
        self.longitude = None
        if gedcomFile is None:
            return
        if len(gedcomFile) == 0:
            return

        for line in gedcomFile:
            # print(f'\t{line}')
            tags = line.split()
            if tags[1] == 'PLAC':
                self.place = line[7:]
            elif tags[1] == 'ADDR':
                self.address = line[7:]
            elif tags[1] == 'CTRY':
                self.country = line[7:]
            elif tags[1] == 'MAP':
                pass
            elif tags[1] == 'LATI':
                self.latitude = line[7:]
            elif tags[1] == 'LONG':
                self.longitude = line[7:]
            else:
                # Unknown.
                print(f'Place unrecogised tag \'{tags[1]}\'')



    def toLongString(self):
        ''' Returns the GedCom date as a long string. '''
        result = ''

        if self.place is not None:
            result = self.place

        if self.address is not None:
            if not self.address in result:
                result = self.address + ', ' + result
        if self.country is not None:
            if not self.country in result:
                result = result + ', ' + self.country

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom date as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedComPlace(self, level):
        '''
        Return the object in GedCom format.
        '''
        result = []

        # Return the calculated value.
        return result
