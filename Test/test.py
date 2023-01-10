#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to test the gedcom modules.
'''

# System Libraries.
import os
import sys
import argparse
# import inspect

# Allow imports from parent folder.
currentFolder = os.path.dirname(os.path.abspath(__file__))
parentFolder = os.path.dirname(currentFolder)
sys.path.insert(0, parentFolder)

# From parent folder.
import gedcom_date



def testGedComDate(dateString):
    ''' Test the GedComDate object with the specified value. '''
    print(f'\'{dateString}\'')
    gedComDate = gedcom_date.GedComDate()
    gedComDate.parse(dateString)
    print(f'\t{gedComDate.toLongString()}')
    print(f'\t{gedComDate.toShortString()}')
    print(f'\t\'{gedComDate.toGedComDate()}\'')



def testDates():
    ''' Run some tests on the GedComDate object. '''
    testGedComDate('')
    testGedComDate('UNKNOWN')
    testGedComDate('DEAD')
    testGedComDate('YES')
    testGedComDate('1 JAN 2023')
    testGedComDate('2012')
    testGedComDate('10 MAR 2022')
    testGedComDate('BEF 1 JAN 2023')
    testGedComDate('AFT 1 JAN 2023')
    testGedComDate('ABT 1 JAN 2023')
    testGedComDate('BEF ABT 1 JAN 2023')
    testGedComDate('AFT ABT 1 JAN 2023')
    testGedComDate('<1> JAN 2023')
    testGedComDate('ABT <JAN> 2023')
    testGedComDate('ABT 2023')
    testGedComDate('ABT <2023>')



def main():
    ''' Entry point for the gedcom viewer. '''
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='test', description='Test the python gedcom library.')
    argParse.add_argument('gedcom', nargs='?', help='The gedcom file to view.')
    argParse.add_argument('-d', '--date', help='Test the gedcom date class.', action='store_true')
    args = argParse.parse_args()

    testDates()




if __name__ == '__main__':
    main()
