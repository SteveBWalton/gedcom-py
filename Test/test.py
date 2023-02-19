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
    gedComDate = gedcom_date.GedComDate(dateString)
    print(f'\'{dateString}\' => [\'{gedComDate.toLongString()}\', \'{gedComDate.toShortString()}\', \'{gedComDate.toGedCom()}\']')



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
    testGedComDate('EST 10 APR 2022')
    testGedComDate('CAL BEF MAY 2021')
    testGedComDate('BET APR 1967 AND JUN 1967')
    testGedComDate('bet 1981 and 1987')
    testGedComDate('ABT BET APR 1967 AND JUN 1967')
    testGedComDate('FROM APR 1967 TO JUN 1967')
    testGedComDate('ABT FROM APR 1967 TO JUN 1967')



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
