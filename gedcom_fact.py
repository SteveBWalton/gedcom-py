# -*- coding: utf-8 -*-

'''
Module to support facts in the gedcom python library.
This module implements the :py:class:`GedComFact` class.
'''
# System Libraries.
from enum import Enum

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace




class GedComFact:
    '''
    Class to represent a fact in the gedcom python library.

    :ivar str type: The type of fact.
    :ivar str information: The value of the fact.
    :ivar list(GedComSource): A list of sources for the fact.
    :ivar GedComDate date: The date of the fact.
    :ivar GedComPlace place: The place of the fact.
    '''


    def __init__(self, parent, block = None):
        '''
        Class constructor for the :py:class:`GedComDate` class.
        '''
        # Individual, family or source.  Must have .gedcom member.
        self.parent = parent
        self.parse(block)



    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the parameter.
        The parameter can be a block or a string.
        '''
        self.type = ''
        self.information = ''
        self.sources = []
        self.date = None
        self.place = None
        if gedcomFile is None:
            return

        # Check that the parameter is a block of lines.
        if not isinstance(gedcomFile, list):
            print('FACT gedcomFile is not a list.')
            return

        # Fetch the fact data.
        tags = gedcomFile[0].split()
        self.type = tags[1]
        self.information = gedcomFile[0][gedcomFile[0].index(tags[1]) + len(tags[1]) + 1:]
        # print(f'FACT {self.type} {self.information}')
        if self.information.startswith('GRID: '):
            line = self.information
            self.information = []
            self.information.append(line.split(': '))

        # Fetch the first block.
        block, start = self.parent.gedcom.getNextBlock(gedcomFile, 1)
        while len(block) > 0:
            # Split into tags.
            tags = block[0].split()
            if tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            elif tags[1] == 'DATE':
                self.date = GedComDate(block)
            elif tags[1] == 'PLAC':
                self.place = GedComPlace(block)
            elif tags[1] == 'CONT':
                if isinstance(self.information, list):
                    # Add to existing list.
                    self.information.append(block[0][7:].split(': '))
                else:
                    # Add to existing string.
                    self.information += '\n' + block[0][7:]
            else:
                # Unknown.
                print(f'FACT unrecogised tag \'{tags[1]}\' \'{block[0]}\'')

            # Fetch the next block.
            block, start = self.parent.gedcom.getNextBlock(gedcomFile, start)




    def toLongString(self):
        ''' Returns the GedCom fact as a long string. '''
        result = ''
        if isinstance(self.information, list):
            # Information is a grid.
            result += '<table>'
            for rows in self.information:
                result += '<tr>'
                for cell in rows:
                    result += f'<td style="white-space: nowrap;">\'{cell}\'</td>'
                result += '</tr>'
            result += '</table>'
        else:
            # Normal string information.
            if self.type is not None:
                result += f'{self.type} '
            if self.information is not None:
                result += f'{self.information} '
        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom fact as a short string. '''
        result = ''

        # Return the calculated value.
        return result.strip()



    def toGedCom(self, level = 1):
        ''' Return the object in GedCom format. '''
        result = []
        if isinstance(self.information, list):
            # Grid of information.
            isFirst = True
            for row in self.information:
                line = ': '.join(row)
                if isFirst:
                    result.append(f'{level} {self.type} {line}')
                    isFirst = False
                else:
                    result.append(f'{level + 1} CONT {line}')
        elif '\n' in self.information:
            # Multi line information.
            lines = self.information.split('\n')
            isFirst = True
            for line in lines:
                if isFirst:
                    result.append(f'{level} {self.type} {line}')
                    isFirst = False
                else:
                    result.append(f'{level + 1} CONT {line}')
        else:
            # Expected single line information.
            result.append(f'{level} {self.type} {self.information}')
        if self.date is not None:
            result.append(f'{level + 1} DATE {self.date.toGedCom()}')
            for source in self.date.sources:
                result.append(f'{level + 2} SOUR @{source}@')
        if self.place is not None:
            result.extend(self.place.toGedCom(level))
        for source in self.sources:
            result.append(f'{level + 1} SOUR @{source}@')

        # Return the calculated value.
        return result
