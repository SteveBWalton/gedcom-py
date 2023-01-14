# -*- coding: utf-8 -*-

'''
Module to support sources in the gedcom python library.
This module implements the :py:class:`GedComSource` class.
'''
# System Libraries.
from enum import Enum

# Application Librariess.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_note import GedComNote



''' The type of special sources. '''
class GedComSourceType(Enum):
    GENERAL = 1
    BIRTH_CERTIFICATE = 2
    MARRIAGE_CERTIFICATE = 3
    DEATH_CERTIFICATE = 4



class GedComSource:
    '''
    Class to represent a source in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''


    def __init__(self, gedcom, gedcomFile = None):
        '''
        Class constructor for the :py:class:`GedComSource` class.
        '''
        self.gedcom = gedcom
        self.parse(gedcomFile)



    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the string.
        '''
        self.identity = None
        self.title = ''
        self.type = GedComSourceType.GENERAL
        self.date = None
        self.place = None
        self.note = None
        if gedcomFile is None:
            return
        if len(gedcomFile) == 0:
            return

        # The identity is on the first line.
        tags = gedcomFile[0].split()
        if tags[1][:1] == '@':
            self.identity = tags[1][1:-1]

        # Fetch the first block.
        block, start = self.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            #for line in block:
            #    print(line)
            #print('<--')
            tags = block[0].split()
            if tags[1] == 'TITL':
                self.title = block[0][7:]
            elif tags[1] == 'DATE':
                self.date = GedComDate(block)
            elif tags[1] == 'NOTE':
                self.note = GedComNote(block)
            elif tags[1] == 'PLAC':
                self.place = GedComPlace(block)
            elif tags[1] == 'REPO':
                pass
            else:
                # Unknown.
                print(f'Source unrecogised tag \'{tags[1]}\' \'{block[0]}\'.')

            # Fetch the next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)

        # Debug output.
        print(f'\'{self.identity}\'')



    def toLongString(self):
        ''' Returns the GedCom source as a long string. '''
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
        ''' Returns the GedCom source as a short string. '''
        result = ''

        if self.place is not None:
            result = self.place

        if ',' in result:
            result = result[0:result.index(',')]

        # Return the calculated value.
        return result.strip()



    def toGedCom(self, level):
        '''
        Return the object in GedCom format.
        '''
        result = []

        # Return the calculated value.
        return result
