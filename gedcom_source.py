# -*- coding: utf-8 -*-

'''
Module to support sources in the gedcom python library.
This module implements the :py:class:`GedComSource` class.
'''
# System Libraries.
from enum import Enum
import datetime

# Application Librariess.
from gedcom_fact import GedComFact
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_change import GedComChange



''' The type of special sources. '''
class GedComSourceType(Enum):
    GENERAL = 1
    BIRTH_CERTIFICATE = 2
    MARRIAGE_CERTIFICATE = 3
    DEATH_CERTIFICATE = 4
    CENSUS = 5



class GedComSource:
    '''
    Class to represent a source in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''
    # Connection to the single gedcom.
    gedcom = None



    def byChange(source):
        ''' Key for a list sort of sources by change date order. '''
        if source.change is None:
            return datetime.datetime(1980, 1, 1)
        return source.change.datetime



    def __init__(self, gedcomFile = None):
        ''' Class constructor for the :py:class:`GedComSource` class. '''
        if gedcomFile is None:
            self.identity = f'S{len(GedComSource.gedcom.sources) + 1:04d}'
            self.gedcomFile = ''
            self.title = ''
            self.type = GedComSourceType.GENERAL
            self.repository = ''
            self.date = None
            self.place = None
            self.facts = None
            self.change = None
            return

        # Build the source from gedcom block.
        self.parse(gedcomFile)



    def parse(self, gedcomFile = None):
        ''' Update the object to the date specified in the string. '''
        self.gedcomFile = gedcomFile
        self.identity = None
        self.title = ''
        self.type = GedComSourceType.GENERAL
        self.repository = ''
        self.date = None
        self.place = None
        self.facts = None
        self.change = None
        if gedcomFile is None:
            return
        if len(gedcomFile) == 0:
            return

        # The identity is on the first line.
        tags = gedcomFile[0].split()
        if tags[1][:1] == '@':
            self.identity = tags[1][1:-1]

        # Fetch the first block.
        block, start = GedComSource.gedcom.getNextBlock(gedcomFile, 1)
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
                if self.facts is None:
                    self.facts = []
                self.facts.append(GedComFact(block))
            elif tags[1] == 'PLAC':
                self.place = GedComPlace(block)
            elif tags[1] == 'REPO':
                self.repository = block[0][7:]
                self.repository = self.repository[1:-1]
            elif tags[1] == 'CHAN':
                self.change = GedComChange(block)
            else:
                # Unknown.
                print(f'Source unrecogised tag \'{tags[1]}\' \'{block[0]}\'.')

            # Fetch the next block.
            block, start = GedComSource.gedcom.getNextBlock(gedcomFile, start)

        # Update the source type.
        self.setTypeFromTitle()

        # Debug output.
        # print(f'\'{self.identity}\'')



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



    def toGedCom(self):
        ''' Return the source in GedCom format. '''
        gedcom = []
        gedcom.append(f'0 @{self.identity}@ SOUR')
        gedcom.append(f'1 TITL {self.title}')
        if self.date is not None:
            gedcom.append(f'1 DATE {self.date.toGedCom()}')
        if self.place is not None:
            gedcom.extend(self.place.toGedCom())
        # Facts.
        if self.facts is not None:
            for fact in self.facts:
                gedcom.extend(fact.toGedCom())
        # Repository
        if self.repository != '':
            gedcom.append(f'1 REPO @{self.repository}@')
        # Change.
        if self.change is not None:
            gedcom.extend(self.change.toGedCom(1))

        # Return the calculated value.
        return gedcom



    def getName(self):
        ''' Return the name of the source. '''
        return self.title



    def setTypeFromTitle(self):
        ''' Update the source type from the title. '''
        if self.title.startswith('Marriage'):
            self.type = GedComSourceType.MARRIAGE_CERTIFICATE
        elif self.title.startswith('Birth'):
            self.type = GedComSourceType.BIRTH_CERTIFICATE
        elif self.title.startswith('Death'):
            self.type = GedComSourceType.DEATH_CERTIFICATE
        elif self.title.startswith('Census'):
            self.type = GedComSourceType.CENSUS
        else:
            self.type = GedComSourceType.GENERAL



    def setTitleFromType(self):
        ''' Update the title from the source type. '''
        if self.type == GedComSourceType.GENERAL:
            # Not sure about this.
            return

        if ':' in self.title:
            index = self.title.index(': ')
            self.title = self.title[index+2:]

        if self.type == GedComSourceType.MARRIAGE_CERTIFICATE:
            self.title = f'Marriage Certificate: {self.title}'
        elif self.type == GedComSourceType.BIRTH_CERTIFICATE:
            self.title = f'Birth Certificate: {self.title}'
        elif self.type == GedComSourceType.DEATH_CERTIFICATE:
            self.title = f'Death Certificate: {self.title}'
        elif self.type == GedComSourceType.CENSUS:
            self.title = f'Census: {self.title}'

