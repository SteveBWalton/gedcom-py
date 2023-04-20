# -*- coding: utf-8 -*-

'''
Module to support the configuration options for the gedcom-py project.
This implements the :py:class:`Configuration` class.
'''

import os
import os.path
import platform
import pathlib

# My own libraries.
import walton.xml



class Configuration:
    '''
    Class to represent the configuration options for the gedcom project.
    Originally this used xml.dom.minidom directly but now using my own :py:class:`~walton.xml.XmlDocument` class.

    :ivar string DIRECTORY: The home directory for this user and the gedcom program.
    :ivar string FILENAME: The filename of the configuration file for this user.
    :ivar walton.xml.XmlDocument xmlDocument: The :py:class:`~walton.xml.XmlDocument` object that persists the configuration options.
    :ivar string databaseFilename: The filename of the formula one results database.
    :ivar string flagsDatabaseFilename: The filename of the flags database.
    :ivar string flagsDirectory: The directory that contains the flags images.
    '''



    def __init__(self):
        ''' Class constructor for the :py:class:`Configuration` class. '''
        # Decide the location of the configuration directories and files.
        #if platform.system() == 'Windows':
        #    import pathlib
        #    self.DIRECTORY = str(pathlib.Path.home()) # Does this work in Linux ?
        #    self.FILENAME = self.DIRECTORY + '\\formulaone.xml'
        #else:
        #    self.DIRECTORY = os.getenv('HOME')
        #    self.FILENAME = self.DIRECTORY + '/formulaone.xml'
        self.DIRECTORY = os.path.join(str(pathlib.Path.home()), '.walton', 'gedcom')    # pylint: disable=invalid-name
        self.FILENAME = os.path.join(self.DIRECTORY, 'gedcom-py.xml')                   # pylint: disable=invalid-name

        # Check that the configuration directory exists.
        if not os.path.exists(self.DIRECTORY):
            print(f"Create {self.DIRECTORY}")
            try:
                os.mkdir(self.DIRECTORY)
            except:
                # This will not fix the problem now, but might for the next run!
                parentFolder = os.path.join(str(pathlib.Path.home()), '.walton')
                if not os.path.exists(parentFolder):
                    print(f"Create {parentFolder}")
                    os.mkdir(parentFolder)


        # The XmlDocument object that persits the configuration options.
        self.xmlDocument = walton.xml.XmlDocument(self.FILENAME, 'gedcom')

        # Initialise the standard options.
        self.textSize = 10
        self.colourScheme = 'grey'
        self.fontName = 'Liberation Sans'
        self.verticalSpace = 1
        self.horizontalSpace = 2
        self.isDivider = False

        # Initialise the project specific options.
        self.treeFontSize = 9 # 7
        self.treeTitleFontSize = 12 # 8
        self.treePersonWidth = 200 # 150
        self.treePersonHeight = 60 # 50
        self.treeSpaceX = 30 # 20
        self.treeSpaceY = 50 # 20
        self.treeLineSpace = 12 # 10
        # Add options for the size of boxes and the spacing.

        # Read the options.
        self.readOptions()

        # If a new document then write the document.
        if self.xmlDocument.dirty:
            self.saveConfigurationFile()



    def readOptions(self):
        ''' Read the options from the configuration file. '''
        # Read the database filename
        #xmlDatabase = self.xmlDocument.root.getNode('database')

        # The filename of the formula one results database.
        #if platform.system() == 'Windows':
        #    default = r'\\qnap210\home\Sports\formulaone.sqlite'
        #else:
        #    default = os.getenv("HOME") + '/Documents/Personal/Sports/formulaone.sqlite'
        #self.databaseFilename = xmlDatabase.getAttributeValue('filename', default, True)

        #xmlCountries = self.xmlDocument.root.getNode('flags')

        # The filename of the flags database.
        #if platform.system() == 'Windows':
        #    default = r'\\qnap210\home\Sports\flags.sqlite'
        #else:
        #    default = os.getenv("HOME") + '/Documents/Personal/Sports/flags.sqlite'
        #self.flagsDatabaseFilename = xmlCountries.getAttributeValue('filename', default, True)

        # The directory that contains the flags images.
        #if platform.system() == 'Windows':
        #    default = r'\\qnap210\home\Projects\Graphics\Flags' + "\\"
        #else:
        #    default = os.getenv("HOME") + '/Projects/Graphics/Flags/'
        #self.flagsDirectory = xmlCountries.getAttributeValue('directory', default, True)
        # print(self.flagsDirectory)

        xmlMainWindow = self.xmlDocument.root.getNode('main_window')
        self.textSize = xmlMainWindow.getAttributeValue('text_size', 10, True)
        self.colourScheme = xmlMainWindow.getAttributeValue('colour_scheme', 'grey', True)
        self.fontName = xmlMainWindow.getAttributeValue('font', 'Liberation Sans', True)
        self.verticalSpace = xmlMainWindow.getAttributeValue('vertical_space', 1, True)
        self.horizontalSpace = xmlMainWindow.getAttributeValue('horizontal_space', 2, True)
        self.isDivider = xmlMainWindow.getAttributeValue('divider', False, True)



    def saveConfigurationFile(self):
        ''' Write the configuration file to disk. '''
        self.xmlDocument.save()



    def setTextSize(self, newSize):
        '''
        Set the current text size.

        :param int newSize: Specifies the new text size.
        '''
        # Get the main window node.
        xmlMainWindow = self.xmlDocument.root.getNode('main_window')
        xmlMainWindow.setAttributeValue('text_size', newSize)
        self.textSize = newSize



    def setColourScheme(self, newScheme):
        ''' Set the current colour scheme. '''
        xmlMainWindow = self.xmlDocument.root.getNode('main_window')
        xmlMainWindow.setAttributeValue('colour_scheme', newScheme)
        self.colourScheme = newScheme



    def setFont(self, newFont):
        ''' Set the current font. '''
        # Replace + with space.
        newFont = newFont.replace('+', ' ')

        # Set the font name.
        xmlMainWindow = self.xmlDocument.root.getNode('main_window')
        xmlMainWindow.setAttributeValue('font', newFont)
        self.fontName = newFont



    def setSpace(self, newVertical, newHorizontal):
        ''' Set the vertical and horizontal space. '''
        xmlMainWindow = self.xmlDocument.root.getNode('main_window')
        xmlMainWindow.setAttributeValue('vertical_space', newVertical)
        xmlMainWindow.setAttributeValue('horizontal_space', newHorizontal)
        self.verticalSpace = newVertical
        self.horizontalSpace = newHorizontal



    def setDivider(self, newDivider):
        ''' Set the divider status. '''
        # print('setDivider({})'.format(newDivider))
        xmlMainWindow = self.xmlDocument.root.getNode('main_window')
        self.isDivider = newDivider
        xmlMainWindow.setAttributeValue('divider', self.isDivider)
