# -*- coding: utf-8 -*-

'''
Module to support media in the gedcom python library.
This module implements the :py:class:`GedComMedia` class.
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



class GedComMedia:
    '''
    Class to represent a source in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''
    # Connection to the single gedcom.
    gedcom = None



    def byChange(media):
        ''' Key for a list sort of media by last change. '''
        if media.change is None:
            return datetime.datetime(1980, 1, 1)
        return media.change.datetime



    def __init__(self, gedcom, gedcomFile = None):
        '''
        Class constructor for the :py:class:`GedComSource` class.
        '''
        GedComMedia.gedcom = gedcom
        self.parse(gedcomFile)



    def parseFile(self, block):
        ''' Parse the FILE tag. '''
        for line in block:
            tags = line.split()
            if tags[1] == 'FILE':
                self.file = line[7:]
            elif tags[1] == 'TITL':
                self.title = line[7:]
            elif tags[1] == 'FORM':
                self.form = line[7:]
            elif tags[1] == 'TYPE':
                self.type = line[7:]
            else:
                # Unknown.
                print(f'FILE unrecogised tag \'{tags[1]}\' \'{line}\'.')

            # Fetch the next block.


    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the string.
        '''
        self.gedcomFile = gedcomFile
        self.identity = None
        self.file = None
        self.title = None
        self.form = None
        self.type = None
        self.isPrimary = None
        self.isThumbnail = None
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
        block, start = GedComMedia.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            #for line in block:
            #    print(line)
            #print('<--')
            tags = block[0].split()
            if tags[1] == 'FILE':
                self.parseFile(block)
            elif tags[1] == 'NOTE':
                if self.facts is None:
                    self.facts = []
                self.facts.append(GedComFact(self, block))
            elif tags[1] == 'CHAN':
                self.change = GedComChange(block)
            elif tags[1] == '_PRIM':
                self.isPrimary = tags[2] == 'Y'
            elif tags[1] == '_THUM':
                self.isThumbnail = tags[2] == 'Y'
            else:
                # Unknown.
                print(f'Media unrecogised tag \'{tags[1]}\' \'{block[0]}\'.')

            # Fetch the next block.
            block, start = GedComMedia.gedcom.getNextBlock(gedcomFile, start)

        # Debug output.
        # print(f'\'{self.identity}\'')



    def toLongString(self):
        ''' Returns the GedCom source as a long string. '''
        result = ''

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom source as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedCom(self):
        ''' Return the source in GedCom format. '''
        gedcom = []
        gedcom.append(f'0 @{self.identity}@ OBJE')
        if self.file is not None:
            gedcom.append(f'1 FILE {self.file}')
        if self.form is not None:
            gedcom.append(f'2 FORM {self.form}')
        if self.type is not None:
            gedcom.append(f'3 TYPE {self.type}')
        if self.title is not None:
            gedcom.append(f'2 TITL {self.title}')
        if self.isPrimary is not None:
            if self.isPrimary:
                gedcom.append(f'1 _PRIM Y')
            else:
                gedcom.append(f'1 _PRIM N')
        if self.isThumbnail is not None:
            if self.isThumbnail:
                gedcom.append(f'1 _THUM Y')
            else:
                gedcom.append(f'1 _THUM N')
        # Return the calculated value.
        return gedcom



    def toImage(self, height=0):
        ''' Return the media object as a html image. '''
        if height == 0:
            return f'<img src="file://{GedComMedia.gedcom.mediaFolder}{self.file}" />'
        return f'<img src="file://{GedComMedia.gedcom.mediaFolder}{self.file}" height="{height}" />'



    def getName(self):
        ''' Return the name of the source. '''
        return self.title



