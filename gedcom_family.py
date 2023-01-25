# -*- coding: utf-8 -*-

'''
Module to support a family in the gedcom python library.
This module implements the :py:class:`GedComFamily` class.
'''

# System libraries.
from enum import Enum
import datetime

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_fact import GedComFact
from gedcom_change import GedComChange


class IndividualSex(Enum):
    MALE = 1
    FEMALE = 2



class GedComFamily:
    '''
    Class to represent a family in the gedcom python library.

    :ivar string identity: The identity of the family in the gedcom file.
    :ivar GedCom gedcom: The gedcom object that contains this family.
    '''



    def __init__(self, gedcom, gedcomFile = None):
        ''' Class constructor for a family in a gedcom file. '''
        self.gedcom = gedcom
        self.parse(gedcomFile)



    def parse(self, gedcomFile):
        ''' Build the family from the specified gedcom settings. '''
        # The default empty settings.
        self.gedcomFile = gedcomFile
        self.identity = ''
        self.husbandIdentity = None
        self.wifeIdentity = None
        self.childrenIdentities = []
        self.marriage = None
        self.divorce = None
        self.change = None
        self.sources = []
        if gedcomFile is None:
            return

        # The identity is on the first line.
        tags = gedcomFile[0].split()
        if tags[1][:1] == '@':
            self.identity = tags[1][1:-1]

        # Fetch the first block.
        block, start = self.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            tags = block[0].split()
            if tags[1] == 'MARR':
                # This gives the type, date and place.
                self.marriage = GedComFact(self, block)
            elif tags[1] == 'HUSB':
                self.husbandIdentity = tags[2][1:-1]
            elif tags[1] == 'WIFE':
                self.wifeIdentity = tags[2][1:-1]
            elif tags[1] == 'CHIL':
                self.childrenIdentities.append(tags[2][1:-1])
            elif tags[1] == 'DIV':
                self.divorce = GedComFact(self, block)
            elif tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            elif tags[1] == 'OBJE':
                pass
            elif tags[1] == 'CHAN':
                self.change = GedComChange(block)
            else:
                # Unknown.
                print(f'Family unrecogised tag \'{tags[1]}\'')

            # Fetch next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)

        # Debug output.
        #childrenName = ''
        #for childIdentity in self.childrenIdentities:
        #    child = self.gedcom.individuals[childIdentity]
        #    childrenName += f', \'{child.givenName}\'';

        #print(f'\'{self.identity}\', \'{self.getName()}\', \'{childrenName}')



    def toGedCom(self):
        ''' Returns the calculated gedcom description of this family. '''
        gedcom = []
        gedcom.append(f'0 @{self.identity}@ FAM')
        if self.wifeIdentity is not None:
            gedcom.append(f'1 WIFE @{self.wifeIdentity}@')
        if self.husbandIdentity is not None:
            gedcom.append(f'1 HUSB @{self.husbandIdentity}@')
        # Marriage.
        if self.marriage is not None:
            gedcom.extend(self.marriage.toGedCom())
        if self.divorce is not None:
            gedcom.extend(self.divorce.toGedCom())
        # Children.
        for child in self.childrenIdentities:
            gedcom.append(f'1 CHIL @{child}@')
        # General sources.
        for source in self.sources:
            gedcom.append(f'1 SOUR @{source}@')
        # Change
        gedcom.extend(self.change.toGedCom(1))

        # Return calculated gedcom.
        return gedcom



    def getName(self):
        ''' Returns a name for this family. '''
        husbandName = None
        if self.husbandIdentity is not None:
            husband = self.gedcom.individuals[self.husbandIdentity]
            husbandName = husband.getName()

        wifeName = None
        if self.wifeIdentity is not None:
            wife = self.gedcom.individuals[self.wifeIdentity]
            wifeName = wife.getName()

        return f'{husbandName} & {wifeName}'



    def byChange(self, family):
        ''' Key for a list sort of families by last change. '''
        if family.change is None:
            return datetime.datetime(1980, 1, 1)
        return family.change.datetime

