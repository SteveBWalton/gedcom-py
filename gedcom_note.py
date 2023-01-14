# -*- coding: utf-8 -*-

'''
Module to support notes in the gedcom python library.
This module implements the :py:class:`GedComNotes` class.
'''
# System Libraries.
import re
from enum import Enum





class GedComNote:
    '''
    Class to represent a date in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''


    def __init__(self, dateString = None):
        '''
        Class constructor for the :py:class:`GedComDate` class.
        '''
        self.parse(dateString)



    def parse(self, block = None):
        '''
        Update the object to the date specified in the parameter.
        The parameter can be a block or a string.
        '''
        self.lines = []
        if block is None:
            return

        # Check that the parameter is a block of lines.
        if not isinstance(block, list):
            return

        for line in block:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == 'NOTE':
                # Add a line.
                self.lines.append(line[7:])
            elif tags[1] == 'CONT':
                # Add a line.
                self.lines.append(line[7:])
            else:
                # Unknown.
                print(f'NOTE unrecogised tag \'{tags[1]}\'')



    def getGrid(self):
        ''' Returns the note as a grid of elements. '''
        grid = []
        for line in self.lines:
            # Split by ':' or '-'
            columns = re.split(':|-', line)
            grid.append(columns)

        # Return the grid.
        return grid


    def toLongString(self):
        ''' Returns the GedCom note as a long string. '''
        result = ''

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom note as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedCom(self):
        '''
        Return the object in GedCom format.
        '''
        result = ''

        # Return the calculated value.
        return result.strip()
