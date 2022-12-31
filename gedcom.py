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
from enum import Enum

# Application libraries.
import walton.install
import walton.ansi

class GedComObjects(Enum):
    INDIVIDUAL = 1
    FAMILY = 2
    MEDIA = 3
    SOURCE = 4
    REPOSITORY = 5
    UNKNOWN = 99



class GedCom:
    ''' Class to represent a GedCom file. '''
    def open(self, fileName):
        ''' Open the specified gedcom file. '''
        file = open(fileName, 'r')
        objectType = GedComObjects.UNKNOWN
        objectLines = []
        self.individuals = []
        self.families = []
        self.media = []
        self.sources = []
        line = file.readline().rstrip('\n')
        while line != '':
            if line[:1] == '0':
                if objectType == GedComObjects.INDIVIDUAL:
                    # Add a new individual.
                    self.individuals.append(1)
                elif objectType == GedComObjects.FAMILY:
                    self.families.append(1)
                elif objectType == GedComObjects.MEDIA:
                    self.media.append(1)
                elif objectType == GedComObjects.SOURCE:
                    self.sources.append(1)
                else:
                    pass
                    # print('Unknown Gedcom object.')

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
                else:
                    print(line[-4:])
                    objectType = GedComObjects.UNKNOWN
                objectLines = []
                objectLines.append(line)
            else:
                # Add line to current group.
                objectLines.append(line)



            # Read the next line.
            line = file.readline().rstrip('\n')
        file.close()

        print(f'There are {len(self.individuals)} individuals, {len(self.families)} families, {len(self.media)} media and {len(self.sources)} sources.')



def main():
    ''' Entry point for the gedcom viewer. '''
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='gedcom', description='Database of results in formula one.')
    argParse.add_argument('gedcom', nargs='?', help='The gedcom file to view.')
    argParse.add_argument('-i', '--install', help='Install the program and desktop link.', action='store_true')
    argParse.add_argument('-u', '--uninstall', help='Uninstall the program.', action='store_true')
    args = argParse.parse_args()

    # Welcome message.
    print(f'{walton.ansi.LIGHT_YELLOW}Gedcom Viewer{walton.ansi.RESET_ALL} by Steve Walton © 2022-2023')
    print(f'Python Version {sys.version_info.major}·{sys.version_info.minor}·{sys.version_info.micro} (expecting 3).')
    print(f'Operating System is {walton.ansi.LIGHT_YELLOW}{platform.system()}{walton.ansi.RESET_ALL}.  Desktop is {walton.ansi.LIGHT_YELLOW}{os.environ.get("DESKTOP_SESSION")}{walton.ansi.RESET_ALL}.')

    # print(dir(args))
    if args.gedcom is None:
        args.gedcom = "/home/steve/Documents/Personal/Family Tree/walton.ged"

    print(f'File to view is {walton.ansi.LIGHT_YELLOW}{args.gedcom}{walton.ansi.RESET_ALL}.')

    gedCom = GedCom()
    gedCom.open(args.gedcom)



if __name__ == '__main__':
    main()
