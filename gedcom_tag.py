# -*- coding: utf-8 -*-

'''
Module to support tags in the gedcom python library.
This module implements the :py:class:`GedComTag` class.
'''
# System Libraries.
from enum import Enum

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace




class GedComTag:
    '''
    Class to represent a tag in the gedcom python library.

    :ivar str type: The type of tag.
    :ivar str information: The value of the tag.
    :ivar list(GedComSource): A list of sources for the tag.
    :ivar GedComDate date: The date of the tag.
    :ivar GedComPlace place: The place of the tag.
    '''

    # Connection to the gedcom.
    gedcom = None

    # The labels for GedComTags.
    tagToLabel_ = {
        'DATE' : 'Date',
        'PLAC' : 'Place',
        'ADDR' : 'Address',
        'BIRT' : 'Birth',
        'DEAT' : 'Death',
        'OCCU' : 'Occupation',
        'EDUC' : 'Education',
        'NOTE' : 'Note',
        'CONT' : 'Continue',
        'MARR' : 'Marriage',
        'TYPE' : 'Type',
        'DIV'  : 'Divorce',
        # Non standard tags.
        '_TODO' : 'ToDo',
        # My own tags!
        'NOTE GRID:' : 'Grid',
    }

    # The gedcom tags for for labels.
    labelToTag_ = dict(map(reversed, tagToLabel_.items()))

    def tagToLabel(tagName):
        if tagName in GedComTag.tagToLabel_:
            return GedComTag.tagToLabel_[tagName]
        return tagName



    def labelToTag(labelName):
        if labelName in GedComTag.labelToTag_:
            return GedComTag.labelToTag_[labelName]
        return labelName



    def __init__(self, block = None):
        ''' Class constructor for the :py:class:`GedComDate` class. '''
        self.parse(block)



    def parse(self, gedcomFile = None):
        '''
        Update the object to the date specified in the parameter.
        The parameter can be a block or a string.
        '''
        self.type = ''
        self.information = ''
        self.sources = []
        # The date associated with this tag.
        self.date = None
        # The place associated with this tag.
        self.place = None
        # List of sub tags of this tag.
        self.tags = None
        if gedcomFile is None:
            return

        # Check that the parameter is a block of lines.
        if not isinstance(gedcomFile, list):
            print('GedComTag gedcomFile is not a list.')
            return

        # Fetch the tag data.
        tags = gedcomFile[0].split()
        self.type = tags[1]
        self.information = gedcomFile[0][gedcomFile[0].index(tags[1]) + len(tags[1]) + 1:]
        # print(f'TAG {self.type} {self.information}')
        if self.information.startswith('GRID: '):
            line = self.information
            self.information = []
            self.information.append(line.split(': '))

        # Fetch the first block.
        block, start = GedComTag.gedcom.getNextBlock(gedcomFile, 1)
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
                    theFullLine = block[0][7:]
                    # Pickup any following CONT tags as line breaks into this row.
                    if len(block) > 1:
                        for extra in range(1, len(block)):
                            # print(f'Extra CONT \'{block[extra][7:]}\'')
                            theFullLine = f'{theFullLine}\n{block[extra][7:]}'
                    # Add a row to the existing list.
                    self.information.append(theFullLine.split(': '))
                else:
                    # Add as a child tag.
                    if self.tags is None:
                        self.tags = []
                    self.tags.append(GedComTag(block))
            elif tags[1] == 'CAUS' or tags[1] == 'TYPE':
                # Add as a child tag.
                if self.tags is None:
                    self.tags = []
                self.tags.append(GedComTag(block))
            else:
                # Unknown.
                print(f'TAG unrecogised tag \'{tags[1]}\' \'{block[0]}\'')

            # Fetch the next block.
            block, start = GedComTag.gedcom.getNextBlock(gedcomFile, start)




    def toLongString(self):
        ''' Returns the GedCom tag as a long string. '''
        result = ''
        if isinstance(self.information, list):
            # Information is a grid.
            result += '<table class="grid" align="center" cellpadding="5" cellspacing="0">'
            isFirst = True
            for rows in self.information:
                result += '<tr>'
                rowCount = 0
                for cell in rows:
                    if isFirst:
                        # This is expected to be 'GRID'.
                        isFirst = False
                    else:
                        if cell == '.':
                            # This represents NULL for an empty cell.
                            result += f'<td></td>'
                        else:
                            result += f'<td class="gridcell{rowCount % 2}" style="white-space: nowrap;">{cell}</td>'
                        rowCount += 1
                result += '</tr>'
            result += '</table>'
        else:
            # Normal string information.
            # if self.type is not None:
            #    result += f'{self.type} '
            if self.information is not None:
                result += f'{self.information}'
            if self.tags is not None:
                for tag in self.tags:
                    if tag.type == 'CONT':
                        result += f' {tag.information}'
        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom tag as a short string. '''
        result = ''
        if self.information is not None:
            result += self.information
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
                    if '\n' in line:
                        isFirst = True
                        lines = line.split('\n')
                        for cell in lines:
                            if isFirst:
                                result.append(f'{level + 1} CONT {cell}')
                                isFirst = False
                            else:
                                result.append(f'{level + 2} CONT {cell}')
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
            if self.date.sources is not None:
                for source in self.date.sources:
                    result.append(f'{level + 2} SOUR @{source}@')
        if self.place is not None:
            result.extend(self.place.toGedCom(level + 1))
        if self.tags is not None:
            for tag in self.tags:
                result.extend(tag.toGedCom(level + 1))
        for source in self.sources:
            result.append(f'{level + 1} SOUR @{source}@')

        # Return the calculated value.
        return result
