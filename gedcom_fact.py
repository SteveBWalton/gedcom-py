# -*- coding: utf-8 -*-

'''
Module to support facts in the gedcom python library.
This module implements the :py:class:`GedComFact` class.
'''
# System Libraries.
from enum import Enum

# Application libraries.
from gedcom_source import GedComSource
from gedcom_date import GedComDate
from gedcom_place import GedComPlace




class GedComFact:
    '''
    Class to represent a fact in the gedcom python library.

    :ivar str type: The type of fact.
    :ivar str information: The value of the fact.
    :ivar list(GedComSource): A list of sources for the fact.
    :ivar GedComDate date: The date of the fact.
    :ivar GedComPlace place: The place of the fact.
    '''


    def __init__(self, parent, block = None):
        '''
        Class constructor for the :py:class:`GedComDate` class.
        '''
        # Individual or family.  Must have .gedcom member.
        self.parent = parent
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

        # Fetch the fact data.
        tags = gedcomFile[0].split()
        self.type = tags[1]
        self.information = gedcomFile[0][gedcomFile[0].index(tags[1]) + len(tags[1]) + 1:]

        # Fetch the first block.
        block, start = self.parent.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
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
                print(f'FACT unrecogised tag \'{tags[1]}\' \'{block[0]}\'')

            # Fetch the next block.
            block, start = self.parent.gedcom.getNextBlock(gedcomFile, start)




    def toLongString(self):
        ''' Returns the GedCom fact as a long string. '''
        result = ''

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom fact as a short string. '''
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
