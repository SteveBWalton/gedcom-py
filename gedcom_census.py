# -*- coding: utf-8 -*-

'''
Module to support census data in the gedcom python library.
This module implements the :py:class:`GedComCensus` class.
'''
# System Libraries.
from enum import Enum

# Application libraries.
from gedcom_source import GedComSource
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_fact import GedComFact




class GedComCensus:
    '''
    Class to represent a fact in the gedcom python library.

    :ivar list(GedComSource): A list of sources for the census.
    :ivar GedComDate date: The date of the census.
    :ivar GedComPlace place: The place of the census.
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
        self.sources = []
        self.date = None
        self.place = None
        self.facts = None
        if gedcomFile is None:
            return

        # Check that the parameter is a block of lines.
        if not isinstance(gedcomFile, list):
            return

        # Fetch the first block.
        block, start = self.individual.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            # Split into tags.
            tags = block[0].split()
            if tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            elif tags[1] == 'DATE':
                self.date = GedComDate(block)
            elif tags[1] == 'PLAC':
                self.place = GedComPlace(block)
            elif tags[1] == 'OCCU' or tags[1] == 'NOTE':
                if self.facts is None:
                    self.facts = []
                self.facts.append(GedComFact(block))
            else:
                # Unknown.
                print(f'CENS unrecogised tag \'{tags[1]}\'')

            # Fetch the next block.
            block, start = self.individual.gedcom.getNextBlock(gedcomFile, start)




    def toLongString(self):
        ''' Returns the GedCom census as a long string. '''
        result = ''

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom census as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedCom(self, level = 1):
        ''' Return the census in GedCom format. '''
        result = []
        result.append(f'{level} CENS')
        if self.date is not None:
            result.append(f'2 DATE {self.date.toGedCom()}')
        if self.place is not None:
            lines = self.place.toGedCom(level + 1)
            for line in lines:
                result.append(line)
        if self.facts is not None:
            for fact in self.facts:
                lines = fact.toGedCom(level + 1)
                for line in lines:
                    result.append(line)
        if self.sources is not None:
            for source in self.sources:
                result.append(f'{level + 1} SOUR {source}')
        # Return the calculated value.
        return result
