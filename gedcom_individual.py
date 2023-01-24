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
from gedcom_census import GedComCensus
from gedcom_change import GedComChange


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

        names = self.givenName.split(' ')
        self.firstName = names[0]


    def parse(self, gedcomFile):
        ''' Build the individual from the specified gedcomFile settings. '''
        self.gedcomFile = gedcomFile
        self.identity = ''
        self.sources = []
        self.givenName = ''
        self.surname = ''
        self.firstName = ''
        self.nameSources = []
        self.sex = IndividualSex.MALE
        self.birth = None
        self.death = None
        # Families of own marrages.
        self.familyIdentities = []
        # Family of parents marrage.
        self.parentFamilyIdentity = None
        self.todos = None
        self.facts = None
        self.census = None
        self.media = None
        self.change = None
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
                # self.parseBirth(block)
                self.birth = GedComFact(self, block)
            elif tags[1] == 'DEAT':
                # self.parseDeath(block)
                self.death = GedComFact(self, block)
            elif tags[1] == 'FAMS':
                # Family spouse.
                self.familyIdentities.append(IdentitySources(block))
            elif tags[1] == 'FAMC':
                # Family child.
                self.parentFamilyIdentity = tags[2][1:-1]
            elif tags[1] == 'OCCU' or tags[1] == 'EDUC' or tags[1] == 'NOTE':
                if self.facts is None:
                    self.facts = []
                self.facts.append(GedComFact(self, block))
            elif tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            elif tags[1] == 'OBJE':
                if self.media is None:
                    self.media = []
                self.media.append(tags[2][1:-1])
            elif tags[1] == 'CENS':
                if self.census is None:
                    self.census = []
                self.census.append(GedComCensus(self, block))
            elif tags[1] == '_TODO':
                if self.todos is None:
                    self.todos = []
                self.todos.append(ToDo(self, block))
            elif tags[1] == 'CHAN':
                self.change = GedComChange(block)
            else:
                # Unknown.
                print(f'Individual unrecogised tag \'{tags[1]}\' \'{block[0]}\'')

            # Fetch the next block.
            block, start = self.gedcom.getNextBlock(gedcomFile, start)

        # Debug output.
        print(f'\'{self.identity}\', \'{self.givenName}\', \'{self.surname}\'')



    def toGedCom(self):
        ''' Returns the calculated gedcom description of this person. '''
        gedcom = []
        gedcom.append(f'0 @{self.identity}@ INDI')
        gedcom.append(f'1 NAME {self.givenName} /{self.surname}/')
        gedcom.append(f'2 GIVN {self.givenName}')
        gedcom.append(f'2 SURN {self.surname}')
        for source in self.nameSources:
            gedcom.append(f'2 SOUR @{source}@')
        if self.sex == IndividualSex.MALE:
            gedcom.append(f'1 SEX M')
        else:
            gedcom.append(f'1 SEX F')
        # Birth.
        if self.birth is not None:
            gedcom.extend(self.birth.toGedCom(1))
        # Death.
        if self.death is not None:
            gedcom.extend(self.death.toGedCom(1))
        # Parents.
        if self.parentFamilyIdentity is not None:
            gedcom.append(f'1 FAMC @{self.parentFamilyIdentity}@')
        # Families.
        for family in self.familyIdentities:
            gedcom.append(f'1 FAMS @{family.identity}@')
            if family.sources is not None:
                for source in family.sources:
                    gedcom.append(f'2 SOUR @{source}@')
        # Census.
        if self.census is not None:
            for census in self.census:
                gedcom.extend(census.toGedCom())
        # Facts.
        if self.facts is not None:
            for fact in self.facts:
                gedcom.extend(fact.toGedCom())
        # Media.
        if self.media is not None:
            for identity in self.media:
                gedcom.append(f'1 OBJE @{identity}@')
        # ToDos
        if self.todos is not None:
            for todo in self.todos:
                gedcom.append(f'1 _TODO {todo.rank} {todo.description}')
        # General sources.
        for source in self.sources:
            gedcom.append(f'1 SOUR @{source}@')
        # Change.
        gedcom.extend(self.change.toGedCom(1))

        # Return calculated gedcom.
        return gedcom



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
        if self.birth.date is None:
            return 'unknown'
        years = self.getYears(theDate)
        if years > 0:
            return f'{years} years'
        difference = theDate.theDate - self.birth.date.theDate
        return f'{difference.days} days'



    def getYears(self, theDate = None):
        ''' Returns the age of the individual in years on the specified date. '''
        if self.birth.date is None:
            return None
        if theDate == None:
            ageDate = datetime.date.today()
        else:
            ageDate = theDate.theDate
        years = ageDate.year - self.birth.date.theDate.year
        if ageDate.month < self.birth.date.theDate.month or (ageDate.month == self.birth.date.theDate.month and ageDate.day < self.birth.date.theDate.day):
            years -= 1

        return years



    def byDateOfMarriage(self, identitySource):
        ''' Key for a list sort of families by start date order. '''
        identity = identitySource.identity
        family = self.gedcom.families[identity]
        if family.marriage is None:
            return datetime.date.today()
        if family.marriage.date is None:
            return datetime.date.today()
        return family.marriage.date.theDate



    def byDateOfBirth(self, identity):
        ''' Key for a list sort of individuals by date of birth order. '''
        individual = self.gedcom.individuals[identity]
        #if individual.birthDate is None:
        #    return None
        if individual.birth is None:
            return None
        if individual.birth.date is None:
            return None
        return individual.birth.date.theDate



    def getSiblings(self):
        ''' Returns the identities of siblings of the individual. '''
        siblings = []
        if self.parentFamilyIdentity is not None:
            family = self.gedcom.families[self.parentFamilyIdentity]
            if family.husbandIdentity is not None:
                father = self.gedcom.individuals[family.husbandIdentity]
                fatherChildren = father.getChildren()
                for child in fatherChildren:
                    if not child in siblings and not child == self.identity:
                        siblings.append(child)
            if family.wifeIdentity is not None:
                mother = self.gedcom.individuals[family.wifeIdentity]
                motherChildren = mother.getChildren()
                for child in motherChildren:
                    if not child in siblings and not child == self.identity:
                        siblings.append(child)

        # Sort the siblings into date order!
        siblings.sort(key=self.byDateOfBirth)

        # Return the children of mother and father.
        return siblings



    def getChildren(self):
        ''' Returns the identities of children of the individual. '''
        children = []
        for familyIdentity in self.familyIdentities:
            family = self.gedcom.families[familyIdentity.identity]
            for childIdentity in family.childrenIdentities:
                children.append(childIdentity)

        # Sort the children into date order!
        children.sort(key=self.byDateOfBirth)

        # Return the children.
        return children


