# -*- coding: utf-8 -*-

'''
Module to support an individual in the gedcom python library.
This module implements the :py:class:`GedComIndividual` class.
'''

# System libraries.
from enum import Enum

# Application libraries.
from gedcom_date import GedComDate



class IndividualSex(Enum):
    MALE = 1
    FEMALE = 2



class GedComIndividual:
    '''
    Class to represent an individual in the gedcom python library.

    :ivar string identity: The identity of the individual in the gedcom file.
    :ivar GedCom gedcom: The gedcom object that contains this individual.
    :ivar string givenName: The given name of the individual.
    :ivar string surname: The surname of the individual.
    '''



    def __init__(self, gedcom, gedcomFile = None):
        ''' Class constructor for an individual in a gedcom file. '''
        self.gedcom = gedcom
        self.identity = ''
        self.givenName = ''
        self.surname = ''
        self.sex = IndividualSex.MALE
        self.birthDate = GedComDate()
        # Families of own marrage.
        self.familyIdentities = []
        # Family of parents marrage.
        self.parentFamilyIdentity = None
        if gedcomFile != None:
            self.parse(gedcomFile)



    def parseBirth(self, gedcom):
        ''' Build the birth from the specified gedcom settings. '''
        for line in gedcom:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == 'BIRT':
                pass
            elif tags[1] == 'DATE':
                # print(line[7:])
                self.birthDate = GedComDate(line[7:])
            elif tags[1] == 'PLAC':
                pass
            elif tags[1] == 'MAP':
                pass
            elif tags[1] == 'LATI':
                pass
            elif tags[1] == 'LONG':
                pass
            else:
                # Unknown.
                print(f'Individual BIRTH unrecogised tag \'{tags[1]}\'')



    def parseSex(self, gedcom):
        ''' Build the sex from the specified gedcom settings. '''
        for line in gedcom:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == 'SEX':
                if tags[2][0:1] == 'F':
                    self.sex = IndividualSex.FEMALE
            else:
                # Unknown.
                print(f'Individual SEX unrecogised tag \'{tags[1]}\'')



    def parseName(self, gedcom):
        ''' Build the name from the specified gedcom settings. '''
        # Loop through the tags.
        for line in gedcom:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == 'NAME':
                # Ignore this for now.
                pass
            elif tags[1] == 'SURN':
                if len(tags) > 2:
                    self.surname = tags[2]
                    for index in range(3, len(tags)):
                        self.surname += ' ' + tags[index]
            elif tags[1] == 'GIVN':
                if len(tags) > 2:
                    self.givenName = tags[2]
                    for index in range(3, len(tags)):
                        self.givenName += ' ' + tags[index]
            elif tags[1] == 'OCCU':
                # Not sure about this.
                pass
            else:
                # Unknown.
                print(f'Individual NAME unrecogised tag \'{tags[1]}\'')



    def parse(self, gedcomFile):
        ''' Build the individual from the specified gedcomFile settings. '''
        # Add an extra line to flush the final tag.
        gedcomFile.append('1 EXIT')

        # Loop through the tags looking for level 1 tags.
        objectLines = []
        for line in gedcomFile:
            if line[:1] == '1':
                # Deal with the old objectLines.
                tags = objectLines[0].split()
                if tags[1][:1] == '@':
                    self.identity = tags[1][1:-1]
                elif tags[1] == 'NAME':
                    self.parseName(objectLines)
                elif tags[1] == 'SEX':
                    self.parseSex(objectLines)
                elif tags[1] == 'BIRT':
                    self.parseBirth(objectLines)
                elif tags[1] == 'DEAT':
                    pass
                elif tags[1] == 'FAMS':
                    # Family spouse.
                    self.familyIdentities.append(tags[2][1:-1])
                elif tags[1] == 'FAMC':
                    # Family child.  Must add this person as a child of the family.
                    self.parentFamilyIdentity = tags[2][1:-1]
                elif tags[1] == 'SOUR':
                    pass
                elif tags[1] == 'OBJE':
                    pass
                elif tags[1] == 'CENS':
                    pass
                elif tags[1] == 'CHAN':
                    pass
                else:
                    # Unknown.
                    print(f'Individual unrecogised tag \'{tags[1]}\'')

                # Start a new object lines.
                objectLines = []

            # Add line to current group.
            objectLines.append(line)

        # Debug output.
        print(f'\'{self.identity}\', \'{self.givenName}\', \'{self.surname}\', \'{self.birthDate.toLongString()}\', \'{ self.familyIdentities}\', \'{ self.parentFamilyIdentity}\'')



    def getName(self):
        ''' Returns the full name of the individual. '''
        return self.givenName + ' ' + self.surname
