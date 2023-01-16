# -*- coding: utf-8 -*-

'''
Module to support an individual in the gedcom python library.
This module implements the :py:class:`GedComIndividual` class.
'''

# System libraries.
from enum import Enum
import datetime

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_fact import GedComFact


class IndividualSex(Enum):
    MALE = 1
    FEMALE = 2



class ToDo:
    ''' Class to represent a ToDO item. '''
    def __init__(self, individual, block):
        ''' Class constructor for a ToDo item. '''
        self.individual = individual
        self.rank = 100
        self.description = ''
        if block is None:
            return
        if not isinstance(block, list):
            return

        for line in block:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == '_TODO':
                # Add a line.
                self.rank = int(tags[2])
                position = line.find(tags[2]) + len(tags[2]) + 1
                self.description = line[position:]
            else:
                # Unknown.
                print(f'_TODO unrecogised tag \'{tags[1]}\' \'{line}\'')



class IdentitySources:
    ''' Class to represent a identity and sources. '''
    def __init__(self, block):
        ''' Class constructor for a identity sources object. '''
        self.identity = None
        self.sources = None
        if block is None:
            return
        if not isinstance(block, list):
            return

        # Identity in first line.
        tags = block[0].split()
        self.identity = tags[2][1:-1]
        block.pop(0)

        # Loop through the rest of block.
        for line in block:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == 'SOUR':
                if self.sources is None:
                    self.sources = []
                self.sources.append(tags[2][1:-1])
            else:
                # Unknown.
                print(f'Identity Sources unrecogised tag \'{tags[1]}\' \'{line}\'')



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
        self.parse(gedcomFile)



    def parseDeath(self, gedcomFile):
        ''' Build the death from the specified gedcom settings. '''
        # Fetch the first block.
        block, start = self.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            tags = block[0].split()
            if tags[1] == 'DATE':
                self.deathDate = GedComDate(block)
            elif tags[1] == 'PLAC':
                self.deathPlace = GedComPlace(block)
            elif tags[1] == 'SOUR':
                pass
            else:
                # Unknown.
                print(f'Individual DEATH unrecogised tag \'{tags[1]}\'')

            # Fetch next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)



    def parseBirth(self, gedcomFile):
        ''' Build the birth from the specified gedcom settings. '''
        # Fetch the first block.
        block, start = self.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            tags = block[0].split()
            if tags[1] == 'DATE':
                # self.birthDate = GedComDate(block[0][7:])
                self.birthDate = GedComDate(block)
            elif tags[1] == 'PLAC':
                self.birthPlace = GedComPlace(block)
            #elif tags[1] == 'SOUR':
            #    self.birthSources.append(tags[2][1:-1])
            else:
                # Unknown.
                print(f'Individual BIRTH unrecogised tag \'{tags[1]}\'')

            # Fetch next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)



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
            elif tags[1] == 'SOUR':
                self.nameSources.append(tags[2][1:-1])
            else:
                # Unknown.
                print(f'Individual NAME unrecogised tag \'{tags[1]}\'')



    def parse(self, gedcomFile):
        ''' Build the individual from the specified gedcomFile settings. '''
        self.gedcomFile = gedcomFile
        self.identity = ''
        self.sources = []
        self.givenName = ''
        self.surname = ''
        self.nameSources = []
        self.sex = IndividualSex.MALE
        self.birthDate = GedComDate()
        self.birthPlace = None
        self.deathDate = None
        self.deathPlace = None
        # Families of own marrages.
        self.familyIdentities = []
        # Family of parents marrage.
        self.parentFamilyIdentity = None
        self.todos = None
        self.facts = None
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
            if tags[1] == 'NAME':
                self.parseName(block)
            elif tags[1] == 'SEX':
                self.parseSex(block)
            elif tags[1] == 'BIRT':
                self.parseBirth(block)
            elif tags[1] == 'DEAT':
                self.parseDeath(block)
            elif tags[1] == 'FAMS':
                # Family spouse.
                self.familyIdentities.append(IdentitySources(block))
            elif tags[1] == 'FAMC':
                # Family child.
                self.parentFamilyIdentity = tags[2][1:-1]
            elif tags[1] == 'OCCU' or tags[1] == 'EDUC':
                if self.facts is None:
                    self.facts = []
                self.facts.append(GedComFact(self, block))
            elif tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            elif tags[1] == 'OBJE':
                pass
            elif tags[1] == 'CENS':
                pass
            elif tags[1] == '_TODO':
                if self.todos is None:
                    self.todos = []
                self.todos.append(ToDo(self, block))
            elif tags[1] == 'CHAN':
                pass
            else:
                # Unknown.
                print(f'Individual unrecogised tag \'{tags[1]}\'')

            # Fetch the next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)

        # Debug output.
        print(f'\'{self.identity}\', \'{self.givenName}\', \'{self.surname}\', \'{self.birthDate.toLongString()}\'')



    def getName(self):
        ''' Returns the full name of the individual. '''
        return self.givenName + ' ' + self.surname



    def isMale(self):
        ''' Returns True for males. '''
        if self.sex == IndividualSex.FEMALE:
            return False
        return True



    def heShe(self):
        ''' Returns he or she. '''
        if self.sex == IndividualSex.FEMALE:
            return 'she'
        return 'he'



    def hisHer(self):
        ''' Returns he or she. '''
        if self.sex == IndividualSex.FEMALE:
            return 'her'
        return 'his'



    def getAge(self, theDate = None):
        ''' Returns the age of the individual on the specified day. '''
        if self.birthDate is None:
            return 'unknown'
        years = self.getYears(theDate)
        return f'{years} years'



    def getYears(self, theDate = None):
        ''' Returns the age of hte individual in years on the specified date. '''
        if self.birthDate is None:
            return None
        if theDate == None:
            ageDate = datetime.date.today()
        else:
            ageDate = theDate.theDate
        years = ageDate.year - self.birthDate.theDate.year
        if ageDate.month < self.birthDate.theDate.month or (ageDate.month == self.birthDate.theDate.month and ageDate.day == self.birthDate.theDate.day):
            years -= 1

        return years
