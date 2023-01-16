# -*- coding: utf-8 -*-

'''
Module to support facts in the gedcom python library.
This module implements the :py:class:`GedComFact` class.
'''
# System Libraries.
from enum import Enum





class GedComFact:
    '''
    Class to represent a fact in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''


    def __init__(self, individual, block = None):
        '''
        Class constructor for the :py:class:`GedComDate` class.
        '''
        self.individual = individual
        self.parse(block)



    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the parameter.
        The parameter can be a block or a string.
        '''
        self.type = ''
        self.information = ''
        self.sources = []
        self.date = None
        self.place = None
        if gedcomFile is None:
            return

        # Check that the parameter is a block of lines.
        if not isinstance(gedcomFile, list):
            return

        tags = gedcomFile[0].split()
        print(gedcomFile[0])
        self.type = tags[1]
        self.information = gedcomFile[0][gedcomFile[0].index(tags[1]) + len(tags[1]) +1:]
        print(f'FACT type is \'{self.type}\'')
        print(f'FACT information is \'{self.information}\'')

        # Fetch the first block.
        block, start = self.individual.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:

            # print(line)
            # Split into tags.
            tags = block[0].split()
            if tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            elif tags[1] == 'DATE':
                self.date = GedComDate(block)
            elif tags[1] == 'PLAC':
                self.place = GedComPlace(block)
            else:
                # Unknown.
                print(f'FACT unrecogised tag \'{tags[1]}\'')

            # Fetch the next block.
            block, start = self.individual.gedcom.getNextBlock(gedcomFile, start)




    def toLongString(self):
        ''' Returns the GedCom note as a long string. '''
        result = ''

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom note as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedCom(self):
        '''
        Return the object in GedCom format.
        '''
        result = ''

        # Return the calculated value.
        return result.strip()
