# -*- coding: utf-8 -*-

'''
Module to support places in the gedcom python library.
These Place objects are not part of gedcom.
It is intended that a GedComPlace is a hierarchical composition of Place objects.
This module implements the :py:class:`Place` class.
'''
# System Libraries.
from enum import Enum



class PlaceType(Enum):
    PLACE = 1
    ADDRESS = 2
    COUNTRY = 3



class Place:
    '''
    Class to represent a single place in a GedComPlace object.

    :ivar GedComDateStatus status: The status of the date, EMPTY, ON, BEFORE, AFTER.
    :ivar GedComDateAccuracy accuracy: The accuracy of the date, KNOWN, ABOUT, ESTIMATED, CALCULATED
    '''
    allPlaces = {}

    def getPlace(placeName, address = None, country = None):
        ''' Get the place object for the specified name. '''
        print(f'getPlace({placeName})')
        if ', ' in placeName:
            parent = placeName[placeName.index(', ') + 2:]
            name = placeName[0: placeName.index(', ')]
        else:
            parent = None
            name = placeName

        # Return the existing place.
        if name in Place.allPlaces:
            return Place.allPlaces[name]

        # Return a new place.
        return Place(placeName, address, country)



    def byName(place):
        ''' Key for a list sort of places by name. '''
        return place.name



    def __init__(self, gedcomFile = None, address = None, country = None):
        ''' Class constructor for the :py:class:`Place` class. '''
        self.parse(gedcomFile, address, country)



    def parse(self, gedcom = None, address = None, country = None):
        ''' Update the object to the date specified in the string. '''
        self.placeType = PlaceType.PLACE
        self.parent = None
        self.name = ''

        if ', ' in gedcom:
            parent = gedcom[gedcom.index(', ') + 2:]
            self.parent = Place.getPlace(parent)
            self.name = gedcom[0: gedcom.index(', ')]
        else:
            self.name = gedcom

        if self.name == country:
            self.placeType = PlaceType.COUNTRY
        if self.name == address:
            self.placeType = PlaceType.ADDRESS
        Place.allPlaces[self.name] = self
        print(f'name = {self.name}')



    def toLongString(self):
        ''' Returns the GedCom date as a long string. '''
        result = ''

        if self.name is not None:
            result = self.name

        if self.parent is not None:
            result = f'{result}, {self.parent.toLongString()}'

        # Return the calculated value.
        return result.strip()




    def toShortString(self):
        ''' Returns the GedCom date as a short string. '''
        result = ''

        if self.place is not None:
            result = self.place

        if ',' in result:
            result = result[0:result.index(',')]

        # Return the calculated value.
        return result.strip()



    def toGedCom(self, level = 1):
        '''
        Return the object in GedCom format.
        '''
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
