# -*- coding: utf-8 -*-

'''
Module to support a family in the gedcom python library.
This module implements the :py:class:`GedComFamily` class.
'''

# System libraries.
from enum import Enum

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace



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



    def parseMarriage(self, gedcomFile):
        ''' Parse the marriage tags which might not be a marriage. '''
        # Fetch the first block.
        block, start = self.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            tags = block[0].split()
            if tags[1] == 'DATE':
                self.startDate = GedComDate(block)
            elif tags[1] == 'PLAC':
                self.startPlace = GedComPlace(block)
            else:
                # Unknown.
                print(f'Family MARR unrecogised tag \'{tags[1]}\' \'{block[0]}\'.')

            # Fetch next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)



    def parse(self, gedcomFile):
        ''' Build the family from the specified gedcom settings. '''
        # The default empty settings.
        self.identity = ''
        self.husbandIdentity = None
        self.wifeIdentity = None
        self.childrenIdentities = []
        self.startDate = None
        self.startPlace = None
        if gedcomFile is None:
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
            if tags[1] == 'MARR':
                # This gives the type, date and place.
                self.parseMarriage(block)
            elif tags[1] == 'HUSB':
                self.husbandIdentity = tags[2][1:-1]
            elif tags[1] == 'WIFE':
                self.wifeIdentity = tags[2][1:-1]
            elif tags[1] == 'CHIL':
                self.childrenIdentities.append(tags[2][1:-1])
            elif tags[1] == 'SOUR':
                pass
            elif tags[1] == 'OBJE':
                pass
            elif tags[1] == 'CHAN':
                pass
            else:
                # Unknown.
                print(f'Family unrecogised tag \'{tags[1]}\'')

            # Fetch next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)

        # Debug output.
        startDate = None
        if self.startDate is not None:
            startDate = self.startDate.toGedComDate()

        husbandName = None
        if self.husbandIdentity is not None:
            husband = self.gedcom.individuals[self.husbandIdentity]
            husbandName = husband.givenName + ' ' + husband.surname

        wifeName = None
        if self.wifeIdentity is not None:
            wife = self.gedcom.individuals[self.wifeIdentity]
            wifeName = wife.givenName + ' ' + wife.surname

        childrenName = ''
        for childIdentity in self.childrenIdentities:
            child = self.gedcom.individuals[childIdentity]
            childrenName += f', \'{child.givenName}\'';

        print(f'\'{self.identity}\', \'{startDate}\', \'{husbandName}\', \'{wifeName}\'{childrenName}')
