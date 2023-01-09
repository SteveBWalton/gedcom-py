# -*- coding: utf-8 -*-

'''
Module to support dates in the gedcom python library.
This module implements the :py:class:`GedComDate` class.
'''
# System Libraries.
import datetime
from enum import Enum



class GedComDateStatus(Enum):
    EMPTY = 1
    ON = 2
    BEFORE = 3
    AFTER = 4

    KNOWN = 101
    GUESS = 102
    UNKNOWN = 103




class GedComDate:
    '''
    Class to represent a date in the gedcom python library.
    '''


    def __init__(self):
        '''
        Class constructor for the :py:class:`GedComDate` class.
        '''
        self.status = GedComDateStatus.EMPTY
        self.isAbout = False
        self.dayStatus = GedComDateStatus.UNKNOWN
        self.monthStatus = GedComDateStatus.UNKNOWN
        self.yearStatus = GedComDateStatus.UNKNOWN
        # pub is_month_quarter: bool,
        self.theDate = datetime.date.today()



    def parse(self, dateString):
        '''
        Update the object to the date specified in the string.
        '''
        if dateString == '' or dateString.upper() == 'UNKNOWN':
            self.status = GedComDateStatus.EMPTY
            return

        # If FROM .. TO or BET ... AND then deal with each half separately.

        # Default status.
        self.status = GedComDateStatus.ON
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        month = None
        numberOne = None
        numberTwo = None
        numberOneGuess = False
        numberTwoGuess = False
        blocks = dateString.split()
        for block in blocks:
            # print(f'\t\'{block}\'')
            isGuess = False
            if block[:1] == '<':
                # Guess.
                isGuess = True
                block = block[1:]
            if block[-1:] == '>':
                # Guess close.
                block = block[:-1]
                # print(f'\t\'{block}\'')
            if block == 'BEF':
                self.status = GedComDateStatus.BEFORE
            elif block == 'AFT':
                self.status = GedComDateStatus.AFTER
            elif block == 'ABT':
                self.isAbout = True
            elif block in months:
                month = months.index(block) + 1
                if isGuess:
                    self.monthStatus = GedComDateStatus.GUESS
                else:
                    self.monthStatus = GedComDateStatus.KNOWN
            else:
                try:
                    number = int(block)
                except:
                    # Not a number ignore.
                    pass
                else:
                    numberTwo = numberOne
                    numberTwoGuess = numberOneGuess
                    numberOne = number
                    numberOneGuess = isGuess

        if numberOne is None:
            self.yearStatus = GedComDateStatus.UNKNOWN
            year = 2023

            # Not sure about this.
            self.status = GedComDateStatus.EMPTY
            return

        else:
            year = numberOne
            if numberOneGuess:
                self.yearStatus = GedComDateStatus.GUESS
            else:
                self.yearStatus = GedComDateStatus.KNOWN

        if month is None:
            self.monthStatus = GedComDateStatus.UNKNOWN
            month = 1

        if numberTwo is None:
            day = 1
            self.dayStatus = GedComDateStatus.UNKNOWN
        else:
            day = numberTwo
            if numberTwoGuess:
                self.dayStatus = GedComDateStatus.GUESS
            else:
                self.dayStatus = GedComDateStatus.KNOWN

        self.theDate = datetime.date(year, month, day)




    def toLongString(self):
        ''' Returns the GedCom date as a long string. '''
        if self.status == GedComDateStatus.EMPTY:
            return 'Unknown'
        elif self.status == GedComDateStatus.BEFORE:
            result = 'before '
        elif self.status == GedComDateStatus.AFTER:
            result = 'after '
        else:
            result = 'on '
        # Between is another possibility for later.

        if self.isAbout:
            result = f'{result}about '

        if self.dayStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%-d").strip()} '
        elif self.dayStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%-d").strip()}> '
        if self.monthStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%B")} '
        elif self.monthStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%B")}> '
        if self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%Y")}'
        elif self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}<{self.theDate.strftime("%Y")}>'


        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom date as a short string. '''
        if self.status == GedComDateStatus.EMPTY:
            return 'Unknown'
        elif self.status == GedComDateStatus.BEFORE:
            result = 'before '
        elif self.status == GedComDateStatus.AFTER:
            result = 'after '
        else:
            result = 'on '
        # Between is another possibility for later.

        if self.isAbout:
            result = f'{result}about '

        if self.dayStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%-d").strip()} '
        elif self.dayStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%-d").strip()}> '
        if self.monthStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%b")} '
        elif self.monthStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%b")}> '
        if self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%y")}'
        elif self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}<{self.theDate.strftime("%y")}>'

        # Return the calculated value.
        return result.strip()



    def toGedComDate(self):
        '''
        Return the object in GedCom format.
        '''
        if self.status == GedComDateStatus.EMPTY:
            return 'UNKNOWN'
        elif self.status == GedComDateStatus.BEFORE:
            result = 'BEF '
        elif self.status == GedComDateStatus.AFTER:
            result = 'AFT '
        else:
            result = ''
        # Between is another possibility for later.

        if self.isAbout:
            result = f'{result}ABT '

        if self.dayStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%-d").strip()} '
        elif self.dayStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%-d").strip()}> '
        if self.monthStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%b").upper()} '
        elif self.monthStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%b").upper()}> '
        if self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%Y")}'
        elif self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}<{self.theDate.strftime("%Y")}>'

        # Return the calculated value.
        return result.strip()
