# -*- coding: utf-8 -*-

'''
Module to support places in the gedcom python library.
This module implements the :py:class:`GedComPlace` class.
'''
# System Libraries.
from enum import Enum

# Application Libraries.
from place import Place



class GedComPlaceAccuracy(Enum):
    KNOWN = 1
    ABOUT = 2
    ESTIMATED = 3
    CALCULATED = 4



class GedComPlace:
    '''
    Class to represent a place in the gedcom python library.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''


    def __init__(self, gedcomFile = None):
        '''
        Class constructor for the :py:class:`GedComPlace` class.
        '''
        self.parse(gedcomFile)



    def parse(self, gedcomFile = None):
        ''' Update the object to the date specified in the string. '''
        self.place = None
        self.address = None
        self.country = None
        self.latitude = None
        self.longitude = None
        self.sources = []
        if gedcomFile is None:
            return
        if len(gedcomFile) == 0:
            return

        for line in gedcomFile:
            # print(f'\t{line}')
            tags = line.split()
            if tags[1] == 'PLAC':
                self.place = line[7:]
            elif tags[1] == 'ADDR':
                self.address = line[7:]
            elif tags[1] == 'CTRY':
                self.country = line[7:]
            elif tags[1] == 'MAP':
                pass
            elif tags[1] == 'LATI':
                self.latitude = line[7:]
            elif tags[1] == 'LONG':
                self.longitude = line[7:]
            elif tags[1] == 'SOUR':
                self.sources.append(tags[2][1:-1])
            else:
                # Unknown.
                print(f'Place unrecogised tag \'{tags[1]}\'')

        if self.address is None or self.address == '':
            place = Place.getPlace(self.place, self.address, self.country, self.latitude, self.longitude)
        else:
            place = Place.getPlace(f'{self.address}, {self.place}', self.address, self.country, self.latitude, self.longitude)



    def toLongString(self):
        ''' Returns the GedCom place as a long html string. '''
        result = ''

        if self.place is not None:
            result = self.place

        if self.address is not None:
            if not self.address in result:
                result = self.address + ', ' + result
        if self.country is not None:
            if not self.country in result:
                result = result + ', ' + self.country

        placeName = result.strip()
        result = ''
        while ', ' in placeName:
            place = Place.getPlace(placeName)
            if result == '':
                result = f'<a href="app:place?id={place.identity}">{place.name}</a>'
            else:
                result = f'{result}, <a href="app:place?id={place.identity}">{place.name}</a>'

            # Remove first comma.
            placeName = placeName[placeName.index(', ') + 2:]

        # Add the final place.
        place = Place.getPlace(placeName)
        if result == '':
            result = f'<a href="app:place?id={place.identity}">{place.name}</a>'
        else:
            result = f'{result}, <a href="app:place?id={place.identity}">{place.name}</a>'

        # Return the calculated value.
        return result



    def toIdentityCheck(self):
        ''' Returns the GedCom place as a string for identity checks. '''
        result = ''

        if self.place is not None:
            result = self.place

        if self.address is not None:
            if not self.address in result:
                result = self.address + ', ' + result

        # Return the calculated value.
        return result.strip()



    def toShortString(self):
        ''' Returns the GedCom place as a short string. '''
        result = ''

        if self.place is not None:
            result = self.place

        if ',' in result:
            result = result[0:result.index(',')]

        # Return the calculated value.
        return result.strip()



    def toGedCom(self, level = 1):
        ''' Return the object in GedCom format. '''
        result = []
        result.append(f'{level} PLAC {self.place}')
        if self.address is not None:
            result.append(f'{level + 1} ADDR {self.address}')
        if self.latitude is not None or self.longitude is not None:
            result.append(f'{level + 1} MAP')
        if self.latitude is not None:
            result.append(f'{level + 2} LATI {self.latitude}')
        if self.longitude is not None:
            result.append(f'{level + 2} LONG {self.longitude}')
        if self.country is not None:
            result.append(f'{level + 1} CTRY {self.country}')
        for source in self.sources:
            result.append(f'{level + 1} SOUR @{source}@')

        # Return the calculated value.
        return result
