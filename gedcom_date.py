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
    BETWEEN = 5
    FROM = 6
    NOT_ON = 9

    KNOWN = 101
    GUESS = 102
    UNKNOWN = 103

class GedComDateAccuracy(Enum):
    KNOWN = 1
    ABOUT = 2
    ESTIMATED = 3
    CALCULATED = 4


class GedComDate:
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



    def __lt__(self, other):
        ''' Magic Method to define < behaviour. '''
        if self.theDate is None:
            return True
        if other is None:
            return False
        if other.theDate is None:
            return False
        return self.theDate < other.theDate



    def parse(self, dateString = None):
        '''
        Update the object to the date specified in the parameter.
        The parameter can be a block or a string.
        '''
        self.the2ndDate = None
        self.sources = []
        if dateString is None:
            return

        if isinstance(dateString, str):
            return self.parseString(dateString)

        if not isinstance(dateString, list):
            return

        for line in dateString:
            # print(line)
            # Split into tags.
            tags = line.split()
            if tags[1] == 'DATE':
                self.parseString(line[7:])
            elif tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            else:
                # Unknown.
                print(f'DATE unrecogised tag \'{tags[1]}\'')



    def parseString(self, dateString = None):
        '''
        Update the object to the date specified in the string.
        '''
        if dateString == '' or dateString.upper() == 'UNKNOWN':
            self.status = GedComDateStatus.EMPTY
            return

        # If FROM .. TO or BET ... AND then deal with each half separately.
        if 'BET' in dateString:
            index = dateString.index('AND')
            afterString = dateString[index+4:]
            beforeString = dateString[:index-1]
            self.the2ndDate = GedComDate(afterString)
            self.the2ndDate.status = GedComDateStatus.NOT_ON
            dateString = beforeString
        if 'FROM' in dateString:
            index = dateString.index('TO')
            afterString = dateString[index+3:]
            beforeString = dateString[:index-1]
            self.the2ndDate = GedComDate(afterString)
            self.the2ndDate.status = GedComDateStatus.NOT_ON
            dateString = beforeString

        # Default accuracy.
        self.accuracy = GedComDateAccuracy.KNOWN

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
            #print(f'\t\'{block}\'')
            isGuess = False
            if block[:1] == '<':
                # Guess.
                isGuess = True
                block = block[1:]
            if block[-1:] == '>':
                # Guess close.
                block = block[:-1]
                #print(f'\t\'{block}\'')
            if block == 'BEF':
                self.status = GedComDateStatus.BEFORE
            elif block == 'AFT':
                self.status = GedComDateStatus.AFTER
            elif block == 'BET':
                self.status = GedComDateStatus.BETWEEN
            elif block == 'FROM':
                self.status = GedComDateStatus.FROM
            elif block == 'ABT':
                self.accuracy = GedComDateAccuracy.ABOUT
            elif block == 'EST':
                self.accuracy = GedComDateAccuracy.ESTIMATED
            elif block == 'CAL':
                self.accuracy = GedComDateAccuracy.CALCULATED
            elif block.upper() in months:
                month = months.index(block.upper()) + 1
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
            # print(f'year is {year}')
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

        #print(f'date({year}, {month}, {day})')
        self.theDate = datetime.date(year, month, day)
        #print(f'theDate = {self.theDate}')




    def toLongString(self):
        ''' Returns the GedCom date as a long string. '''
        if self.status == GedComDateStatus.EMPTY:
            return 'unknown'
        elif self.status == GedComDateStatus.BEFORE:
            result = 'before '
        elif self.status == GedComDateStatus.AFTER:
            result = 'after '
        elif self.status == GedComDateStatus.BETWEEN:
            result = 'between '
        elif self.status == GedComDateStatus.FROM:
            result = 'from '
        elif self.status == GedComDateStatus.NOT_ON:
            result = ''
        else:
            result = 'on '
        # Between is another possibility for later.

        if self.accuracy == GedComDateAccuracy.ABOUT:
            result = f'{result}about '
        elif self.accuracy == GedComDateAccuracy.ESTIMATED:
            result = f'{result}estimated '
        elif self.accuracy == GedComDateAccuracy.CALCULATED:
            result = f'{result}calculated '

        if self.dayStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%-d").strip()} '
        elif self.dayStatus == GedComDateStatus.GUESS:
            result = f'{result}({self.theDate.strftime("%-d").strip()}) '
        if self.monthStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%B")} '
        elif self.monthStatus == GedComDateStatus.GUESS:
            result = f'{result}({self.theDate.strftime("%B")}) '
        if self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%Y")}'
        elif self.yearStatus == GedComDateStatus.GUESS:
            result = f'{result}({self.theDate.strftime("%Y")})'

        if self.status == GedComDateStatus.BETWEEN:
            result = f'{result.strip()} and {self.the2ndDate.toLongString()}'
        if self.status == GedComDateStatus.FROM:
            result = f'{result.strip()} to {self.the2ndDate.toLongString()}'

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom date as a short string. '''
        if self.status == GedComDateStatus.EMPTY:
            return 'unknown'
        elif self.status == GedComDateStatus.BEFORE:
            result = '<'
        elif self.status == GedComDateStatus.AFTER:
            result = '>'
        elif self.status == GedComDateStatus.BETWEEN:
            result = 'bet '
        elif self.status == GedComDateStatus.FROM:
            result = 'bet '
        elif self.status == GedComDateStatus.NOT_ON:
            result = ''
        else:
            result = 'on '
        # Between is another possibility for later.

        #if self.accuracy == GedComDateAccuracy.ABOUT:
        #    result = f'{result}about '
        #elif self.accuracy == GedComDateAccuracy.ESTIMATED:
        #    result = f'{result}estimated '
        #elif self.accuracy == GedComDateAccuracy.CALCULATED:
        #    result = f'{result}calculated '

        if self.dayStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%-d").strip()} '
        elif self.dayStatus == GedComDateStatus.GUESS:
            result = f'{result}({self.theDate.strftime("%-d").strip()}) '
        if self.monthStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%b")} '
        elif self.monthStatus == GedComDateStatus.GUESS:
            result = f'{result}({self.theDate.strftime("%b")}) '
        if self.yearStatus == GedComDateStatus.KNOWN:
            result = f'{result}{self.theDate.strftime("%y")}'
        elif self.yearStatus == GedComDateStatus.GUESS:
            result = f'{result}({self.theDate.strftime("%y")})'

        if self.status == GedComDateStatus.BETWEEN:
            result = f'{result.strip()}/{self.the2ndDate.toShortString()}'
        if self.status == GedComDateStatus.FROM:
            result = f'{result.strip()}/{self.the2ndDate.toShortString()}'

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
        elif self.status == GedComDateStatus.BETWEEN:
            result = 'BET '
        elif self.status == GedComDateStatus.FROM:
            result = 'FROM '
        elif self.status == GedComDateStatus.NOT_ON:
            result = ''
        else:
            result = ''
        # Between is another possibility for later.

        if self.accuracy == GedComDateAccuracy.ABOUT:
            result = f'{result}ABT '
        elif self.accuracy == GedComDateAccuracy.ESTIMATED:
            result = f'{result}EST '
        elif self.accuracy == GedComDateAccuracy.CALCULATED:
            result = f'{result}CAL '

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
        elif self.yearStatus == GedComDateStatus.GUESS:
            result = f'{result}<{self.theDate.strftime("%Y")}>'

        if self.status == GedComDateStatus.BETWEEN:
            result = f'{result.strip()} AND {self.the2ndDate.toGedComDate()}'
        if self.status == GedComDateStatus.FROM:
            result = f'{result.strip()} TO {self.the2ndDate.toGedComDate()}'

        # Return the calculated value.
        return result.strip()
