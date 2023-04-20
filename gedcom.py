#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to open a gedcom file.
'''

# System libraries.
import sys
import os
import argparse
import platform
import subprocess
import datetime
from enum import Enum

# Application libraries.
import walton.install
import walton.ansi
from application import Application
import widget_wx.main_window
from gedcom_date import GedComDate
from gedcom_individual import GedComIndividual
from gedcom_family import GedComFamily
from gedcom_source import GedComSource
from gedcom_media import GedComMedia
from gedcom_tag import GedComTag
from place import Place



class GedComObjects(Enum):
    INDIVIDUAL = 1
    FAMILY = 2
    MEDIA = 3
    SOURCE = 4
    REPOSITORY = 5
    HEADER = 6
    UNKNOWN = 99



class GedCom:
    '''
    Class to represent a gedcom file.

    :ivar dict(GedComIndividual) individuals: Collection of individuals in this gedcom.
    :ivar dict(GedComFamily) families: Collection of families in this gedcom.
    :ivar string defaultIdentity: The identity of the default individual.
    '''



    def __init__(self):
        ''' Class constructor for GedCom objects. '''
        self.defaultIdentity = None
        self.individuals = {}
        self.families = {}
        self.media = {}
        self.sources = {}
        self.fileName = None
        self.isDirty = False
        Place.allPlaces = {}
        GedComIndividual.gedcom = self
        GedComFamily.gedcom = self
        GedComSource.gedcom = self
        GedComTag.gedcom = self



    def new(self):
        ''' Start a new empty gedcom. '''
        self.defaultIdentity = None
        self.individuals = {}
        self.families = {}
        self.media = {}
        self.sources = {}
        self.fileName = None
        self.isDirty = False
        Place.allPlaces = {}



    def getNextBlock(self, gedcom, start):
        ''' Returns the next block and next position in the gedcom lines or empty list at the end. '''
        block = []
        if start >= len(gedcom):
            return block, start

        level = gedcom[start][:1]
        # print(f'level = {level}')
        block.append(gedcom[start])
        # print(f'\t{gedcom[start]}')
        start += 1
        while start < len(gedcom) and gedcom[start][:1] > level:
            # print(f'\t{gedcom[start]}')
            block.append(gedcom[start])
            start += 1

        # Return the block and the next start position.
        return block, start



    def open(self, fileName):
        ''' Open the specified gedcom file. '''
        print(f'open(\'{fileName}\')')
        file = open(fileName, 'r')
        objectType = GedComObjects.UNKNOWN
        objectLines = []
        self.fileName = fileName
        self.mediaFolder = '/home/steve/Documents/Waltons/Family Tree/'
        self.defaultIdentity = None
        self.individuals = {}
        self.families = {}
        self.media = {}
        self.sources = {}
        Place.allPlaces = {}
        line = file.readline().rstrip('\n')
        while line != '':
            if line[:1] == '0':
                if objectType == GedComObjects.INDIVIDUAL:
                    # Add a new individual.
                    individual = GedComIndividual(objectLines)
                    if len(self.individuals) == 0:
                        self.defaultIdentity = individual.identity
                    self.individuals[individual.identity] = individual
                elif objectType == GedComObjects.FAMILY:
                    family = GedComFamily(objectLines)
                    self.families[family.identity] = family
                elif objectType == GedComObjects.SOURCE:
                    source = GedComSource(objectLines)
                    self.sources[source.identity] = source
                elif objectType == GedComObjects.MEDIA:
                    media = GedComMedia(self, objectLines)
                    self.media[media.identity] = media
                elif objectType == GedComObjects.REPOSITORY:
                    pass
                elif objectType == GedComObjects.HEADER:
                    pass
                else:
                    if len(objectLines) > 0:
                        print('Unknown Gedcom object.')
                        print(f'\t{objectLines[0]}')

                # Start a new object.
                if line[-4:] == 'INDI':
                    objectType = GedComObjects.INDIVIDUAL
                elif line[-3:] == 'FAM':
                    objectType = GedComObjects.FAMILY
                elif line[-4:] == 'OBJE':
                    objectType = GedComObjects.MEDIA
                elif line[-4:] == 'SOUR':
                    objectType = GedComObjects.SOURCE
                elif line[-4:] == 'REPO':
                    objectType = GedComObjects.REPOSITORY
                elif line[-4:] == 'HEAD':
                    # Gedcom Header, tag at the start of a gedcom file.
                    objectType = GedComObjects.HEADER
                elif line[-4:] == 'TRLR':
                    # Gedcom Trailer, tag at the end of a gedcom file.
                    objectType = GedComObjects.UNKNOWN
                else:
                    print(line[-4:])
                    objectType = GedComObjects.UNKNOWN
                objectLines = []

            # Add line to current group.
            objectLines.append(line)

            # Read the next line.
            line = file.readline().rstrip('\n')
        file.close()

        # Sort the familes by date order.
        for individual in self.individuals.values():
            individual.familyIdentities.sort(key=individual.byDateOfMarriage)

        self.isDirty = False

        print(f'There are {len(self.individuals)} individuals, {len(self.families)} families, {len(self.media)} media and {len(self.sources)} sources.')



    def save(self):
        ''' Save the current gedcom with with current file name. '''
        return self.saveAs(self.fileName)




    def writeLines(self, file, lines):
        ''' Write lines into the specified file with line feeds. '''
        for line in lines:
            file.write(f'{line}\n')




    def saveAs(self, fileName):
        ''' Save the current gedcom with the specified file name. '''
        print(f'Save gedcom as {fileName}')
        file = open(fileName, 'w')

        # Write the file header.
        file.write('0 HEAD\n')
        file.write('1 SOUR gedcom-py\n')
        file.write('2 NAME gedcom-py\n')
        file.write('2 VERS 1.0.0\n')
        file.write('1 DEST DISKETTE\n')
        now = datetime.datetime.now()
        file.write(f'1 DATE {now.day} {now.strftime("%b").upper()} {now.year}\n')
        file.write(f'2 TIME {now.strftime("%H:%M:%S")}\n')
        file.write('1 CHAR UTF-8\n')
        file.write(f'1 FILE {os.path.basename(fileName)}\n')

        # Write the individuals.
        for individual in self.individuals.values():
            self.writeLines(file, individual.toGedCom())

        # Write the familes.
        for family in self.families.values():
            self.writeLines(file, family.toGedCom())

        # Write the sources.
        for source in self.sources.values():
            self.writeLines(file, source.toGedCom())

        # Write the media.
        for media in self.media.values():
            self.writeLines(file, media.toGedCom())

        # Write the repositories.
        file.write('0 @R0001@ REPO\n')
        file.write('1 NAME Steve Walton\n')
        file.write('0 @R0002@ REPO\n')
        file.write('1 NAME Genes Reunited\n')
        file.write('1 WWW www.genesreunited.co.uk\n')

        # Close the file.
        file.write('0 TRLR\n')
        file.close()

        self.isDirty = False



def isGraphicsAvailable():
    ''' Returns true if the graphical display is available. '''
    if platform.system() == 'Windows':
        # Graphics are always available under Windows.
        return True
    with subprocess.Popen(["xset", "-q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        process.communicate()
        return process.returncode == 0
    return False



def main():
    ''' Entry point for the gedcom viewer. '''
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='gedcom', description='Database of results in formula one.')
    argParse.add_argument('gedcom', nargs='?', help='The gedcom file to view.')
    argParse.add_argument('-i', '--install', help='Install the program and desktop link.', action='store_true')
    argParse.add_argument('-u', '--uninstall', help='Uninstall the program.', action='store_true')
    args = argParse.parse_args()

    if args.install:
        # Install the program.

        # Global installation.
        walton.install.makeCommandPrompt('gedcom', False, __file__)
        walton.install.makeMenuCategory('waltons', 'Waltons', 'Waltons', True)
        walton.install.makeDesktopFile('walton.gedcom', False, 'Gedcom viewer', __file__, f'{os.path.dirname(__file__)}/formulaone.ico', 'A gedcom file viewer.', 'GNOME;GTK;Waltons;')
        sys.exit(0)

        # Add an alias to remove warning messages.
        walton.install.addBashAlias('gedcom')

    if args.uninstall:
        # Remove the program.
        # Global files.
        walton.install.removeCommandPrompt('gedcom', False)
        walton.install.removeDesktopFile('walton.gedcom', False)
        sys.exit(0)

    # Welcome message.
    print(f'{walton.ansi.LIGHT_YELLOW}Gedcom Viewer{walton.ansi.RESET_ALL} by Steve Walton © 2022-2023')
    print(f'Python Version {sys.version_info.major}·{sys.version_info.minor}·{sys.version_info.micro} (expecting 3).')
    print(f'Operating System is {walton.ansi.LIGHT_YELLOW}{platform.system()}{walton.ansi.RESET_ALL}.  Desktop is {walton.ansi.LIGHT_YELLOW}{os.environ.get("DESKTOP_SESSION")}{walton.ansi.RESET_ALL}.')

    # print(dir(args))
    if args.gedcom is None:
        args.gedcom = "/home/steve/Documents/Personal/Family Tree/walton.ged"

    print(f'File to view is {walton.ansi.LIGHT_YELLOW}{args.gedcom}{walton.ansi.RESET_ALL}.')

    gedCom = GedCom()
    if os.path.exists(args.gedcom):
        gedCom.open(args.gedcom)
    else:
        print(f"'{args.gedcom}' is missing.")

    application = Application(args, gedCom)

    if isGraphicsAvailable():
        # Run via wxPython main window.
        wxApp = widget_wx.main_window.WxApp(application)
        application.postRenderPage = wxApp.frame.displayCurrentPage
        application.actions = wxApp.frame.actions

        # Inspection debugging.
        # import wx.lib.inspection
        # wx.lib.inspection.InspectionTool().Show()

        # wxPython loop.
        wxApp.runMainLoop()
    else:
        print('Error - Graphics are not available.')




if __name__ == '__main__':
    main()
