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

    def getPlace(placeName, address = None, country = None, latitude = None, longitude = None):
        ''' Get the place object for the specified name. '''
        # print(f'getPlace({placeName})')
        # Return the existing place.
        if placeName in Place.allPlaces:
            thePlace = Place.allPlaces[placeName]
            if address is not None and placeName.startswith(address) and thePlace.placeType == PlaceType.PLACE:
                # print(f'\'{placeName}\' convert to an address.')
                thePlace.placeType = PlaceType.ADDRESS
            if latitude is not None and thePlace.latitude is None:
                # print(f'\'{placeName}\' add latitude.')
                latitude = latitude.replace('N', '')
                latitude = latitude.replace('S', '-')
                thePlace.latitude = float(latitude)
            if longitude is not None and thePlace.longitude is None:
                # print(f'\'{placeName}\' add longitude.')
                longitude = longitude.replace('W', '')
                longitude = longitude.replace('E', '-')
                thePlace.longitude = float(longitude)
            return thePlace
        # print(f'\'{placeName}\' does not exist.  Creating now.')

        if ', ' in placeName:
            parent = placeName[placeName.index(', ') + 2:]
            name = placeName[0: placeName.index(', ')]
        else:
            parent = None
            name = placeName

        # Return a new place.
        return Place(name, placeName, address, country, latitude, longitude)



    def byName(place):
        ''' Key for a list sort of places by name. '''
        return place.name



    def __init__(self, name, identity, address = None, country = None, latitude = None, longitude = None):
        ''' Class constructor for the :py:class:`Place` class. '''
        self.parse(name, identity, address, country, latitude, longitude)



    def parse(self, name, identity, address = None, country = None, latitude = None, longitude = None):
        ''' Update the object to the date specified in the string. '''
        self.identity = identity
        self.placeType = PlaceType.PLACE
        self.parent = None
        self.latitude = None
        if isinstance(latitude, str):
            latitude = latitude.replace('N', '')
            latitude = latitude.replace('S', '-')
            self.latitude = float(latitude)
        self.longitude = None
        if isinstance(longitude, str):
            longitude = longitude.replace('W', '')
            longitude = longitude.replace('E', '-')
            self.longitude = float(longitude)
        self.name = name

        if ', ' in identity:
            parent = identity[identity.index(', ') + 2:]
            self.parent = Place.getPlace(parent)

        if self.name == country:
            self.placeType = PlaceType.COUNTRY
        if self.name == address:
            self.placeType = PlaceType.ADDRESS

        Place.allPlaces[self.identity] = self
        # print(f'name = {self.name}, identity={self.identity}')



    def toLongString(self):
        ''' Returns the place as a long string. '''
        result = f'<a href="app:place?id={self.identity}">{self.name}</a>'
        if self.parent is not None:
            result = f'{result}, {self.parent.toLongString()}'
        return result




    def toShortString(self):
        ''' Returns the place as a short string. '''
        return self.name
