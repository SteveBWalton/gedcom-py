# -*- coding: utf-8 -*-

'''
Module to support changes in the gedcom python library.
This module implements the :py:class:`GedComChange` class.
'''
# System Libraries.
import datetime
import os

# Application libraries.




class GedComChange:
    '''
    Class to represent a change in the gedcom python library.

    :ivar DateTime datetime: The date and time of the change.
    :ivar str by: The name person who made the change.
    '''


    def __init__(self, block = None):
        ''' Class constructor for the :py:class:`GedComDate` class. '''
        # Individual or family.  Must have .gedcom member.
        self.datetime = None
        self.by = None
        self.parse(block)



    def setNow(self):
        ''' Update the GedComChange object to now. '''
        self.datetime = datetime.datetime.now()
        self.by = os.getlogin()



    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the parameter.
        The parameter can be a block or a string.
        '''
        self.datetime = None
        self.by = None
        if gedcomFile is None:
            return

        # Check that the parameter is a block of lines.
        if not isinstance(gedcomFile, list):
            return

        date = '1 Jan 1980'
        time = '00:00:00'
        # Fetch the data.
        for line in gedcomFile:
            # Split into tags.
            tags = line.split()
            if tags[1] == 'CHAN':
                pass
            elif tags[1] == 'DATE':
                date = line[7:]
            elif tags[1] == 'TIME':
                time = line[7:]
            elif tags[1] == '_PGVU':
                self.by = line[8:]
            else:
                # Unknown.
                print(f'Change unrecogised tag \'{tags[1]}\' \'{line}\'')
        self.datetime = datetime.datetime.strptime(f'{date} {time}', '%d %b %Y %H:%M:%S')



    def toLongString(self):
        ''' Returns the change as a long string. '''
        result = f'{self.datetime.day} {self.datetime.strftime("%B %Y %H:%M:%S")} by {self.by}'

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the change as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedCom(self, level):
        ''' Return the change in GedCom format. '''
        result = []
        result.append(f'{level} CHAN')
        result.append(f'{level+1} DATE {self.datetime.day} {self.datetime.strftime("%b").upper()} {self.datetime.year}')
        result.append(f'{level+2} TIME {self.datetime.strftime("%H:%M:%S")}')
        result.append(f'{level+1} _PGVU {self.by}')

        # Return the calculated value.
        return result
