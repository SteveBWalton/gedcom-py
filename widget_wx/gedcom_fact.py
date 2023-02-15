# -*- coding: utf-8 -*-

'''
Module to support gedcom facts in the wxPython library.
'''

# System libraries.

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_fact import GedComFact



def addFactToTree(tree, root, fact):
    ''' Adds a gedcom fact to tree under the specified node. '''
    if isinstance(fact, GedComFact):
        parent = tree.AppendItem(root, f'{fact.type}: {fact.information}')
        if fact.date is not None:
            addFactToTree(tree, parent, fact.date)
        if fact.place is not None:
            addFactToTree(tree, parent, fact.place)
        if fact.facts is not None:
            for childFact in fact.facts:
                addFactToTree(tree, parent, childFact)
    elif isinstance(fact, GedComDate):
        parent = tree.AppendItem(root, f'DATE: {fact.toGedCom()}')
    elif isinstance(fact, GedComPlace):
        parent = tree.AppendItem(root, f'PLACE: {fact.toIdentityCheck()}')
    else:
        parent = tree.AppendItem(root, 'Unknown Type')
