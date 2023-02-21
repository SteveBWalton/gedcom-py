# -*- coding: utf-8 -*-

'''
Module to support gedcom tags in the wxPython library.
'''

# System libraries.
import wx
import copy

# Application libraries.
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_tag import GedComTag



_tagToLabel = {
    'DATE' : 'Date',
    'PLAC' : 'Place',
    'ADDR' : 'Address',
    'BIRT' : 'Birth',
    'DEAT' : 'Death',
    'OCCU' : 'Occupation',
    'EDUC' : 'Education',
    'NOTE' : 'Note',
    'CONT' : 'Continue',
    'MARR' : 'Marriage',
    'TYPE' : 'Type',
    'DIV'  : 'Divorce',
    '_TODO' : 'ToDo',
}

_labelToTag = dict(map(reversed, _tagToLabel.items()))

def addTagToTree(tree, root, tag):
    ''' Adds a gedcom tag to tree under the specified node. '''
    if isinstance(tag, GedComTag):
        if isinstance(tag.information, list):
            # Special case of NOTE GRID
            parent = None
            for line in tag.information:
                lineAsString = ': '.join(line)
                # Really not sure about the tags to use here.
                if parent is None:
                    parent = tree.AppendItem(root, f'NOTE {lineAsString}')
                else:
                    tree.AppendItem(parent, f'CONT: {lineAsString}')
        else:
            # Normal tag, expect to come here.
            parent = tree.AppendItem(root, f'{tagToLabel(tag.type)}: {tag.information}', data=copy.copy(tag.sources))
            if tag.date is not None:
                addTagToTree(tree, parent, tag.date)
            if tag.place is not None:
                addTagToTree(tree, parent, tag.place)
            if tag.tags is not None:
                for childFact in tag.tags:
                    addTagToTree(tree, parent, childFact)
    elif isinstance(tag, GedComDate):
        parent = tree.AppendItem(root, f'Date: {tag.toGedCom()}', data = copy.copy(tag.sources))
    elif isinstance(tag, GedComPlace):
        parent = tree.AppendItem(root, f'Place: {tag.place}', data = copy.copy(tag.sources))
        if tag.address is not None:
            tree.AppendItem(parent, f'Address: {tag.address}')
    else:
        parent = tree.AppendItem(root, 'Unknown Type')



def getTagFromTree(tree, root, item, parent=None):
    ''' Get a gedcom tag from a tree control item. '''
    itemTag, itemValue = getTagsFromTreeItem(tree, item)
    # print(f'{itemTag} {itemValue}')
    if parent is None:
        print(f'GedComTag(\'{itemTag}\', \'{itemValue}\')')
        tag = GedComTag()
        tag.type = itemTag
        tag.information = itemValue
        tag.sources = getSourcesFromTreeItem(tree, item)
    else:
        if itemTag == 'DATE':
            print(f'\tGedComDate(\'{itemTag}\', \'{itemValue}\')')
            parent.date = GedComDate(itemValue)
            tag = parent.date
            tag.sources = getSourcesFromTreeItem(tree, item)
        elif itemTag == 'PLAC':
            print(f'\tGedComPlace(\'{itemTag}\', \'{itemValue}\')')
            parent.place = GedComPlace()
            parent.place.place = itemValue
            tag = parent.place
            tag.sources = getSourcesFromTreeItem(tree, item)
        elif itemTag == 'ADDR':
            print('\tAdd the address to parent for now')
            parent.address = itemValue
            tag = None
        else:
            print(f'\tGedComTag(\'{itemTag}\', \'{itemValue}\')')
            tag = GedComTag()
            tag.type = itemTag
            tag.information = itemValue
            tag.sources = getSourcesFromTreeItem(tree, item)
            if parent.tags is None:
                parent.tags = []
            parent.tags.append(tag)

    # Add addition information to this tag.
    if tree.ItemHasChildren(item):
        child, cookie = tree.GetFirstChild(item)
        while child.IsOk():
            getTagFromTree(tree, item, child, tag)
            # Get the next child.
            child, cookie = tree.GetNextChild(item, cookie)

    # Return the gedcom tag.
    return tag



def getTagsFromTreeItem(tree, item):
    ''' Return the tag and value from a tree item. '''
    itemText = tree.GetItemText(item)
    index = itemText.index(':')
    itemTag = itemText[0:index]
    itemValue = itemText[index+1:].strip()
    itemTag = labelToTag(itemTag)
    return itemTag, itemValue



def getSourcesFromTreeItem(tree, item):
    ''' Return the sources from a tree item. '''
    sources = tree.GetItemData(item)
    if sources is None:
        sources = []
    return sources



def editTag(tree, parentWindow):
    ''' Edit the selected tag in the specified tree control. '''
    # Get the selected item.
    treeItem = tree.GetSelection()
    if treeItem == tree.GetRootItem():
        # Can not edit the root item.
        return

    itemTag, itemValue = getTagsFromTreeItem(tree, treeItem)
    editTagDialog = EditTag(parentWindow)
    itemValue = editTagDialog.editTag(itemTag, itemValue)
    if itemValue is not None:
        tree.SetItemText(treeItem, f'{tagToLabel(itemTag)}: {itemValue}')



def getNewTagIndividualOptions(tree = None, item = None):
    ''' Returns the list of possible new tags for the specified individual tag item. '''
    options = []
    if item == None:
        # Root options.
        options.append('Death')
        options.append('Occupation')
        options.append('Education')
        options.append('Note')
        options.append('ToDo')
    else:
        # Find the tag.
        itemText = tree.GetItemText(item)
        index = itemText.index(':')
        itemTag = itemText[0:index]
        if itemTag == 'Date' or itemTag == 'ToDo' or itemTag == 'Continue':
            # No tags.
            pass
        elif itemTag == 'Place':
            options.append('Address')
        elif itemTag == 'Death':
            options.append('Date')
            options.append('Place')
            options.append('Cause')
            options.append('Note')
        elif itemTag == 'Note':
            options.append('Continue')
        else:
            # Default options.
            options.append('Date')
            options.append('Place')
            options.append('Note')
    return options



def getNewTagFamilyOptions(tree = None, item = None):
    ''' Returns the list of possible new tags for the specified family tag item. '''
    options = []
    if item == None:
        # Root options.
        options.append('Marriage')
        options.append('Divorce')
        options.append('Note')
    else:
        # Find the tag.
        itemText = tree.GetItemText(item)
        index = itemText.index(':')
        itemTag = itemText[0:index]
        if itemTag == 'Date' or itemTag == 'Continue':
            # No tags.
            pass
        elif itemTag == 'Place':
            options.append('Address')
        elif itemTag == 'Marriage':
            options.append('Date')
            options.append('Place')
            options.append('Type')
            options.append('Note')
        elif itemTag == 'Note':
            options.append('Continue')
        else:
            # Default options.
            options.append('Date')
            options.append('Place')
            options.append('Note')
    return options



def getNewTagSourceOptions(tree = None, item = None):
    ''' Returns the list of possible new tags for the specified source tag item. '''
    options = []
    if item == None:
        # Root options.
        options.append('Note')
        # Not sure about this.
        options.append('GRID')
    else:
        # Find the tag.
        itemText = tree.GetItemText(item)
        index = itemText.index(':')
        itemTag = itemText[0:index]
        if itemTag == 'Date' or itemTag == 'Continue':
            # No tags.
            pass
        elif itemTag == 'Place':
            options.append('Address')
        elif itemTag == 'Note':
            options.append('Continue')
        else:
            # Default options.
            options.append('Date')
            options.append('Place')
            options.append('Note')
    return options



def tagToLabel(tag):
    ''' Returns the item label to use for the specified gedcom tag. '''
    if tag in _tagToLabel:
        return _tagToLabel[tag]
    print(f'Unknown tag \'{tag}\'')
    return tag



def labelToTag(itemLabel):
    ''' Returns the gedcom tag to use the for the specified item label. '''
    if itemLabel in _labelToTag:
        return _labelToTag[itemLabel]
    print(f'Unknown label \'{itemLabel}\'')
    return itemLabel



class EditTag(wx.Dialog):
    ''' Class to represent the dialog to edit an individual tag in gedcom. '''



    def __init__(self, parentWindow):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.

        Class constructor the :py:class:`EditIndividual` class.
        Construct the dialog but do not show it.
        Call :py:func:`editIndividual` or :py:func:`editNewIndividual` to actually show the dialog.
        '''
        # Initialise the base class.
        wx.Dialog.__init__(self, parentWindow, title='Edit Tag', style = wx.RESIZE_BORDER)

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



    def editTag(self, tagTag, tagValue):
        ''' Show the edit tag dialog and allow the user to edit the tag on the tree control. '''
        self.textValue.SetValue(tagValue)
        if self.ShowModal() == wx.ID_OK:
            newValue = self.textValue.GetValue()
            return newValue
        return None
