# -*- coding: utf-8 -*-

'''
Module to support a family in the gedcom python library.
This module implements the :py:class:`GedComFamily` class.
'''

# System libraries.
from enum import Enum

# Application libraries.
from gedcom_date import GedComDate



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
        self.identity = ''
        self.husbandIdentity = None
        self.wifeIdentity = None
        self.childrenIdentities = []
        if gedcomFile != None:
            self.parse(gedcomFile)



    def parse(self, gedcom):
        ''' Build the family from the specified gedcom settings. '''
        # Add an extra line to flush the final tag.
        gedcom.append('1 EXIT')

        # Loop through the tags looking for level 1 tags.
        objectLines = []
        for line in gedcom:
            if line[:1] == '1':
                # Deal with the old objectLines.
                tags = objectLines[0].split()
                if tags[1][:1] == '@':
                    self.identity = tags[1][1:-1]
                elif tags[1] == 'MARR':
                    # This gives the type, date and place.
                    pass
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

                # Start a new object lines.
                objectLines = []

            # Add line to current group.
            objectLines.append(line)

        # Debug output.
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

        print(f'\'{self.identity}\', \'{husbandName}\', \'{wifeName}\'{childrenName}')
