# -*- coding: utf-8 -*-

'''
Module to support an individual in the gedcom python library.
This module implements the :py:class:`GedComIndividual` class.
'''


class GedComIndividual:
    '''
    Class to represent an individual in the gedcom python library.

    :ivar string identity: The identity of the individual in the gedcom file.
    :ivar string givenName: The given name of the individual.
    :ivar string surname: The surname of the individual.
    '''



    def __init__(self, gedcom = None):
        ''' Class constructor for an individual in a gedcom file. '''
        self.identity = ''
        self.givenName = ''
        self.surname = ''
        if gedcom != None:
            self.parse(gedcom)



    def parseName(self, gedcom):
        ''' Build the name from the specified gedcom settings. '''
        for line in gedcom:
            # print(line)

            # Deal with the old objectLines.
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



    def parse(self, gedcom):
        ''' Build the individual from the specified gedcom settings. '''
        objectLines = []
        for line in gedcom:
            if line[:1] == '1':
                # Deal with the old objectLines.
                tags = objectLines[0].split()
                if tags[1][:1] == '@':
                    # Identity.
                    # print(tags[1])
                    self.identity = tags[1][1:-1]
                elif tags[1] == 'NAME':
                    # Name.
                    self.parseName(objectLines)
                elif tags[1] == 'SEX':
                    pass
                elif tags[1] == 'BIRT':
                    pass
                elif tags[1] == 'DEAT':
                    pass
                elif tags[1] == 'FAMS':
                    pass
                elif tags[1] == 'FAMC':
                    pass
                elif tags[1] == 'SOUR':
                    pass
                elif tags[1] == 'OBJE':
                    pass
                elif tags[1] == 'CENS':
                    pass
                else:
                    # Unknown.
                    print(f'Individual unrecogised tag \'{tags[1]}\'')

                # Start a new object lines.
                objectLines = []

            # Add line to current group.
            objectLines.append(line)

        # Debug output.
        print(f'\'{self.identity}\', \'{self.givenName}\', \'{self.surname}\', ')
