# -*- coding: utf-8 -*-

'''
Module to support gedcom facts in the wxPython library.
'''

# System libraries.
import wx
import copy

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_fact import GedComFact



def addFactToTree(tree, root, fact):
    ''' Adds a gedcom fact to tree under the specified node. '''
    if isinstance(fact, GedComFact):
        if isinstance(fact.information, list):
            # Special case of NOTE GRID
            parent = None
            for line in fact.information:
                lineAsString = ': '.join(line)
                # Really not sure about the tags to use here.
                if parent is None:
                    parent = tree.AppendItem(root, f'NOTE {lineAsString}')
                else:
                    tree.AppendItem(parent, f'CONT: {lineAsString}')
        else:
            # Normal fact, expect to come here.
            parent = tree.AppendItem(root, f'{tagToItemLabel(fact.type)}: {fact.information}', data=copy.copy(fact.sources))
            if fact.date is not None:
                addFactToTree(tree, parent, fact.date)
            if fact.place is not None:
                addFactToTree(tree, parent, fact.place)
            if fact.facts is not None:
                for childFact in fact.facts:
                    addFactToTree(tree, parent, childFact)
    elif isinstance(fact, GedComDate):
        parent = tree.AppendItem(root, f'Date: {fact.toGedCom()}', data = copy.copy(fact.sources))
    elif isinstance(fact, GedComPlace):
        parent = tree.AppendItem(root, f'Place: {fact.place}', data = copy.copy(fact.sources))
        if fact.address is not None:
            tree.AppendItem(parent, f'Address: {fact.address}')
    else:
        parent = tree.AppendItem(root, 'Unknown Type')



def getFactFromTree(tree, root, item, parent=None):
    ''' Get a gedcom fact from a tree control item. '''
    itemTag, itemValue = getTagsFromTreeItem(tree, item)
    # print(f'{itemTag} {itemValue}')
    if parent is None:
        print(f'GedComFact(\'{itemTag}\', \'{itemValue}\')')
        fact = GedComFact()
        fact.type = itemTag
        fact.information = itemValue
        fact.sources = getSourcesFromTreeItem(tree, item)
    else:
        if itemTag == 'DATE':
            print(f'\tGedComDate(\'{itemTag}\', \'{itemValue}\')')
            parent.date = GedComDate(itemValue)
            fact = parent.date
            fact.sources = getSourcesFromTreeItem(tree, item)
        elif itemTag == 'PLAC':
            print(f'\tGedComPlace(\'{itemTag}\', \'{itemValue}\')')
            parent.place = GedComPlace()
            parent.place.place = itemValue
            fact = parent.place
            fact.sources = getSourcesFromTreeItem(tree, item)
        elif itemTag == 'ADDR':
            print('\tAdd the address to parent for now')
            parent.address = itemValue
            fact = None
        else:
            print(f'\tGedComFact(\'{itemTag}\', \'{itemValue}\')')
            fact = GedComFact()
            fact.type = itemTag
            fact.information = itemValue
            fact.sources = getSourcesFromTreeItem(tree, item)
            if parent.facts is None:
                parent.facts = []
            parent.facts.append(fact)

    # Add addition information to this fact.
    if tree.ItemHasChildren(item):
        child, cookie = tree.GetFirstChild(item)
        while child.IsOk():
            getFactFromTree(tree, item, child, fact)
            # Get the next child.
            child, cookie = tree.GetNextChild(item, cookie)

    # Return the gedcom fact.
    return fact



def getTagsFromTreeItem(tree, item):
    ''' Return the tag and value from a tree item. '''
    itemText = tree.GetItemText(item)
    index = itemText.index(':')
    itemTag = itemText[0:index]
    itemValue = itemText[index+1:].strip()
    itemTag = ItemLabelToTag(itemTag)
    return itemTag, itemValue



def getSourcesFromTreeItem(tree, item):
    ''' Return the sources from a tree item. '''
    sources = tree.GetItemData(item)
    if sources is None:
        sources = []
    return sources



def editFact(tree, parentWindow):
    ''' Edit the selected fact in the specified tree control. '''
    # Get the selected item.
    treeItem = tree.GetSelection()
    if treeItem == tree.GetRootItem():
        # Can not edit the root item.
        return

    itemTag, itemValue = getTagsFromTreeItem(tree, treeItem)
    editFactDialog = EditFact(parentWindow)
    itemValue = editFactDialog.editFact(itemTag, itemValue)
    if itemValue is not None:
        tree.SetItemText(treeItem, f'{tagToItemLabel(itemTag)}: {itemValue}')



def getNewFactIndividualOptions(item = None):
    ''' Returns the list of possible new facts for the specified individual fact item. '''
    options = []
    if item == None:
        # Root options.
        options.append('Death')
        options.append('Occupation')
        options.append('Education')
        options.append('Note')
        options.append('ToDo')
    else:
        # Special options.
        options.append('Date')
        options.append('Place')
    return options



def getNewFactFamilyOptions(item = None):
    ''' Returns the list of possible new facts for the specified family fact item. '''
    options = []
    if item == None:
        # Root options.
        options.append('Marriage')
        options.append('Divorce')
        options.append('Note')
    else:
        # Special options.
        options.append('Date')
        options.append('Place')
    return options



def getNewFactSourceOptions(item = None):
    ''' Returns the list of possible new facts for the specified source fact item. '''
    options = []
    if item == None:
        # Root options.
        options.append('Note')
        options.append('GRID')
    else:
        # Special options.
        pass
    return options



def tagToItemLabel(tag):
    ''' Returns the item label to use for the specified gedcom tag. '''
    if tag == 'DATE':
        return 'Date'
    if tag == 'PLAC':
        return 'Place'
    if tag == 'ADDR':
        return 'Address'
    if tag == 'BIRT':
        return 'Birth'
    if tag == 'DEAT':
        return 'Death'
    if tag == 'OCCU':
        return 'Occupation'
    if tag == 'EDUC':
        return 'Education'
    if tag == 'NOTE':
        return 'Note'
    if tag == 'MARR':
        return 'Marriage'
    if tag == 'DIV':
        return 'Divorce'
    if tag == '_TODO':
        return 'ToDo'
    return tag



def ItemLabelToTag(itemLabel):
    ''' Returns the gedcom tag to use the for the specified item label. '''
    if itemLabel == 'Date':
        return 'DATE'
    if itemLabel == 'Place':
        return 'PLAC'
    if itemLabel == 'Address':
        return 'ADDR'
    if itemLabel == 'Birth':
        return 'BIRT'
    if itemLabel == 'Death':
        return 'DEAT'
    if itemLabel == 'Occupation':
        return 'OCCU'
    if itemLabel == 'Education':
        return 'EDUC'
    if itemLabel == 'Note':
        return 'NOTE'
    if itemLabel == 'Marriage':
        return 'MARR'
    if itemLabel == 'Divorce':
        return 'DIV'
    if itemLabel == 'ToDo':
        return '_TODO'
    return itemLabel



class EditFact(wx.Dialog):
    ''' Class to represent the dialog to edit an individual fact in gedcom. '''



    def __init__(self, parentWindow):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.

        Class constructor the :py:class:`EditIndividual` class.
        Construct the dialog but do not show it.
        Call :py:func:`editIndividual` or :py:func:`editNewIndividual` to actually show the dialog.
        '''
        # Initialise the base class.
        wx.Dialog.__init__(self, parentWindow, title='Edit Fact', style = wx.RESIZE_BORDER)

        # Add a panel to the dialog.
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Add vertical zones to the panel.
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        panelValue = wx.Panel(self.panel, wx.ID_ANY)
        boxsizerValue = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panelValue, wx.ID_ANY, 'Value')
        boxsizerValue.Add(label, 0, wx.ALL, 2) # | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
        self.textValue = wx.TextCtrl(panelValue, wx.ID_ANY, size=(340,-1))
        boxsizerValue.Add(self.textValue, 0, wx.ALL, 2) #  | wx.ALIGN_LEFT
        panelValue.SetSizer(boxsizerValue)
        self.boxsizer.Add(panelValue, 0, wx.ALL | wx.EXPAND, 2)

        # OK / Cancel buttons.
        panelOk = wx.Panel(self.panel, wx.ID_ANY)
        boxsizerOk = wx.BoxSizer(wx.HORIZONTAL)
        buttonOk = wx.Button(panelOk, wx.ID_OK, 'OK')
        boxsizerOk.Add(buttonOk, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        buttonCancel = wx.Button(panelOk, wx.ID_CANCEL, 'Cancel')
        boxsizerOk.Add(buttonCancel, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        panelOk.SetSizer(boxsizerOk)
        self.boxsizer.Add(panelOk, 0, wx.ALL | wx.EXPAND, 2)

        # Finish the panel.
        self.panel.SetSizer(self.boxsizer)
        self.boxsizer.Fit(self)



    def editFact(self, factTag, factValue):
        ''' Show the edit fact dialog and allow the user to edit the fact on the tree control. '''
        self.textValue.SetValue(factValue)
        if self.ShowModal() == wx.ID_OK:
            newValue = self.textValue.GetValue()
            return newValue
        return None
