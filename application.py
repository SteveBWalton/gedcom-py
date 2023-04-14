#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to represent the core application for the gedcom-py project.
This module implements the :py:class:`Application` class.
This is functionality which all rendering engines will need.
'''

# System libraries.
#import sys
import os
import platform
#import datetime
import shutil

# The program libraries.
import walton.application
import configuration
import render



class Application(walton.application.IApplication):
    '''
    :ivar Render render: The :py:class:`~render.Render` object for the Formula One results database.
    :ivar Database database: The :py:class:`~database.Database` object for the Formula One results database.
    :ivar Configuration configuration: The :py:class:`~configuration.Configuration` object for the Formula One results database.
    :ivar bool showAge: True to add the show age request to each link.
    :ivar YearRange yearRange: The active year range object for the application.
    :ivar string request: The name of the current page.
    :ivar string parameters: The parameters of the current page request.
    :ivar Dictionary actions: This is a dictionary of actions that the main window can handle!
    :ivar Function postRenderPage: This is the function (in main window) that runs after :py:func:`openCurrentPage`.

    Class to represent the core gedcom-py application.
    This class inherits from the :py:class:`~walton.application.IApplication` base class.
    '''



    def __init__(self, args, gedcom):
        '''
        :param object args: The program arguments.

        Class constructor for the :py:class:`Application` class.
        '''
        # Initialise base classes.
        walton.application.IApplication.__init__(self)

        # Initialise member variables.
        self.args = args
        self.request = 'home'
        self.parameters = ''
        # This will be set by the active main window.
        self.postRenderPage = None
        self.decodeLink = None
        # The actions that the application can handle.
        # This will be overwritten by the active main window.
        self.actions = {}
        # Set to true to enable debugging output.
        self.debug = False

        # The Configuration object for the formula one database.
        # This is the application settings and options.
        self.configuration = configuration.Configuration()

        # The gedcom object for the gedcom application.
        self.gedcom = gedcom

        # The Render object for the application.
        # This is the object that renders the application results to html pages for display.
        self.render = render.Render(self)

        # Generate the style sheets.
        self.setStyleSheets()

        # Show the initial page.
        self.currentUri = ''
        self.render.showHome({})



    def openCurrentPage(self):
        '''
        Load the current page as specified by :py:attr:`self.request` and :py:attr:`self.parameters`.
        Add the options from the main window toolbar to the parameters and fetch the page from the :py:attr:`self.render` object.
        This will call :py:func:`displayCurrentPage` if the content changes.
        Display chain is :py:func:`followLocalLink` → :py:func:`openCurrentPage` → :py:func:`displayCurrentPage`.
        '''
        if self.debug:
            print(f'application.openCurrentPage({self.request}, {self.parameters})')

        parameters = self.parameters

        if self.debug:
            print(f"\trequest '{self.request}', parameters '{parameters}'")

        # Build a dictionary from the parameters.
        parametersDictionary = self.decodeParameters(parameters)

        # This is like a switch statement (that Python does not support)
        isNewContent = True
        if self.request in self.actions:
            isNewContent = self.actions[self.request](parametersDictionary)
        if self.request in self.render.actions:
            isNewContent = True
            self.render.actions[self.request](parametersDictionary)
        #else:
        #    # Ask the render engine if it knows what to do.
        #    bNewContent = False
        #    if self.decode_link != None:
        #        bNewContent = self.decode_link(self.request, parameters)

        # Display the content created by the database.
        if self.postRenderPage is not None:
            if isNewContent:
                # self.DisplayCurrentPage()
                self.postRenderPage()

        # Return false so that idle_add does not call here again.
        return False



    def setStyleSheets(self):
        ''' Set the style sheets on the render html object.'''
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Styles')
        sizeStyleSheet = self.generateSizeStyleSheet(os.path.join(folder, 'textsize.txt'), self.configuration.textSize, folder)
        fontStyleSheet = self.generateFontStyleSheet(os.path.join(folder, 'font.txt'), self.configuration.fontName, folder)

        # Generate a space stylesheet.
        spaceStyleSheet = os.path.join(folder, f'gedcom-space-{self.configuration.verticalSpace}{self.configuration.horizontalSpace}.css')
        with open(spaceStyleSheet, 'w', encoding='utf-8') as fileOutput:
            fileOutput.write(f'td {{ padding: {self.configuration.verticalSpace}px {self.configuration.horizontalSpace}px {self.configuration.verticalSpace}px {self.configuration.horizontalSpace}px; }}\n')
        # fileOutput.close()

        # Remove the existing stylesheets.
        self.render.html.stylesheets = []

        # Local window with local files.
        self.render.html.stylesheets.append('file:' + os.path.join(folder, 'gedcom.css'))
        if self.configuration.colourScheme != 'none':
            self.render.html.stylesheets.append('file:' + os.path.join(folder, f'gedcom-{self.configuration.colourScheme}.css'))
        self.render.html.stylesheets.append('file:' + sizeStyleSheet)
        self.render.html.stylesheets.append('file:' + fontStyleSheet)
        self.render.html.stylesheets.append('file:' + spaceStyleSheet)
