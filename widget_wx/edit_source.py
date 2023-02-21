# -*- coding: utf-8 -*-

'''
Module to support the editing of a source in gedcom.
This uses the wx library.
'''

# System Libraries.
import wx
import sqlite3
import datetime
import time
import os
import sys
import copy

# Import my own libraries.
import widget_wx.gedcom_tag as wxtag
from gedcom_source import GedComSourceType
from gedcom_tag import GedComTag
from gedcom_date import GedComDate
from gedcom_place import GedComPlace
from gedcom_change import GedComChange



class EditSource(wx.Dialog):
    ''' Class to represent the dialog to edit a source in gedcom. '''



    def __init__(self, parentWindow, gedcom, identity):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.
        :param GedCom gedcom: Specify the gedcom that contains this source.
        :param str identity: Specify the identity the source.

        Class constructor the :py:class:`EditSource` class.
        Construct the dialog but do not show it.
        Call :py:func:`editSource` to actually show the dialog.
        '''
        # Initialise the base class.
        wx.Dialog.__init__(self, parentWindow, title='Edit Source', style = wx.RESIZE_BORDER)

        # Initialise member variables.
        self.gedcom = gedcom
        self.source = gedcom.sources[identity]

        # Add a panel to the dialog.
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Add vertical zones to the panel.
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # Details group box.
        if self.source.type == GedComSourceType.BIRTH_CERTIFICATE:
            groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Birth Certificate')
            groupDetailsSizer = wx.GridBagSizer(10, 10)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Title')
            groupDetailsSizer.Add(label, pos = (0,0), span = (1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textTitle = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textTitle, pos = (0,1), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
            groupDetailsSizer.Add(label, pos=(1,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textDate = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textDate, pos=(1,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Place')
            groupDetailsSizer.Add(label, pos=(1,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textPlace = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textPlace, pos = (1,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, pos=(2,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textAddress, pos = (2,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
            self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        elif self.source.type == GedComSourceType.MARRIAGE_CERTIFICATE:
            groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Marriage Certificate')
            groupDetailsSizer = wx.GridBagSizer(10, 10)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Title')
            groupDetailsSizer.Add(label, pos = (0,0), span = (1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textTitle = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textTitle, pos = (0,1), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
            groupDetailsSizer.Add(label, pos=(1,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textDate = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textDate, pos=(1,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Place')
            groupDetailsSizer.Add(label, pos=(1,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textPlace = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textPlace, pos = (1,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, pos=(2,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textAddress, pos = (2,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Name')
            groupDetailsSizer.Add(label, pos=(3,1), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Age')
            groupDetailsSizer.Add(label, pos=(3,2), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Profession')
            groupDetailsSizer.Add(label, pos=(3,3), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Residence')
            groupDetailsSizer.Add(label, pos=(3,4), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Groom')
            groupDetailsSizer.Add(label, pos=(4,0), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textGroomName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textGroomName, pos=(4,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textGroomAge = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(50,-1))
            groupDetailsSizer.Add(self.textGroomAge, pos=(4,2), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textGroomProfession = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textGroomProfession, pos=(4,3), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textGroomResidence = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textGroomResidence, pos=(4,4), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Bride')
            groupDetailsSizer.Add(label, pos=(5,0), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textBrideName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textBrideName, pos=(5,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textBrideAge = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(50,-1))
            groupDetailsSizer.Add(self.textBrideAge, pos=(5,2), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textBrideProfession = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textBrideProfession, pos=(5,3), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textBrideResidence = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textBrideResidence, pos=(5,4), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Groom\'s Father')
            groupDetailsSizer.Add(label, pos=(6,0), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textGroomFatherName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textGroomFatherName, pos=(6,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textGroomFatherProfession = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textGroomFatherProfession, pos=(6,3), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Bride\'s Father')
            groupDetailsSizer.Add(label, pos=(7,0), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textBrideFatherName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textBrideFatherName, pos=(7,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textBrideFatherProfession = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textBrideFatherProfession, pos=(7,3), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Witness')
            groupDetailsSizer.Add(label, pos=(8,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textWitness = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textWitness, pos = (8,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'GRO Reference')
            groupDetailsSizer.Add(label, pos=(9,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textGroReference = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textGroReference, pos = (9,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
            self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        elif self.source.type == GedComSourceType.DEATH_CERTIFICATE:
            groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Death Certificate')
            groupDetailsSizer = wx.GridBagSizer(10, 10)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Title')
            groupDetailsSizer.Add(label, pos = (0,0), span = (1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textTitle = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textTitle, pos = (0,1), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
            groupDetailsSizer.Add(label, pos=(1,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textDate = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textDate, pos=(1,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Place')
            groupDetailsSizer.Add(label, pos=(1,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textPlace = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textPlace, pos = (1,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, pos=(2,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textAddress, pos = (2,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
            self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        elif self.source.type == GedComSourceType.CENSUS:
            groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Census')
            groupDetailsSizer = wx.GridBagSizer(10, 10)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Title')
            groupDetailsSizer.Add(label, pos = (0,0), span = (1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textTitle = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textTitle, pos = (0,1), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
            groupDetailsSizer.Add(label, pos=(1,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textDate = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textDate, pos=(1,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Place')
            groupDetailsSizer.Add(label, pos=(1,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textPlace = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textPlace, pos = (1,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, pos=(2,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textAddress, pos = (2,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
            self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        else:
            # General source.
            groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'General Details')
            groupDetailsSizer = wx.FlexGridSizer(5, 2, 5, 5)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Title')
            groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
            self.textTitle = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textTitle, 0, wx.ALL | wx.ALIGN_LEFT, 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Type')
            groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
            self.comboboxType = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=['General', 'Birth Certificate', 'Marriage Certificate', 'Death Certificate', 'Census'])
            groupDetailsSizer.Add(self.comboboxType, 0, wx.ALL | wx.ALIGN_LEFT, 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
            groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            self.textDate = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textDate)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Place')
            groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
            self.textPlace = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textPlace)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textAddress)
            groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
            self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Tags group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Tags')
        self.treeTags = wx.TreeCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(-1, 150), style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS)
        self.treeTags.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelectionChange)
        groupDetails.Add(self.treeTags, 0, wx.ALL | wx.EXPAND, 2)
        panelButtons = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Tag')
        panelButtons.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxNewTag = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=wxtag.getNewTagSourceOptions())
        panelButtons.Add(self.comboboxNewTag)
        buttonAdd = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Add')
        buttonAdd.Bind(wx.EVT_BUTTON, self.onAddTag)
        panelButtons.Add(buttonAdd)
        buttonEdit = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Edit')
        buttonEdit.Bind(wx.EVT_BUTTON, self.onEditTag)
        panelButtons.Add(buttonEdit)
        buttonRemove = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Remove')
        buttonRemove.Bind(wx.EVT_BUTTON, self.onRemoveTag)
        panelButtons.Add(buttonRemove)
        groupDetails.Add(panelButtons)
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

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



    def onTreeSelectionChange(self, event):
        ''' Event handler for the tree control selection changing. '''
        treeItem = self.treeTags.GetSelection()
        # Update the possible child tags.
        if treeItem == self.treeTags.GetRootItem():
            newTagOptions = wxtag.getNewTagSourceOptions()
        else:
            newTagOptions = wxtag.getNewTagSourceOptions(self.treeTags, treeItem)
        self.comboboxNewTag.Clear()
        for option in newTagOptions:
            self.comboboxNewTag.Append(option)

        # Update the layout.
        self.panel.Layout()



    def onAddTag(self, event):
        ''' Event handler for the add tag button click. '''
        # Get the tag type.
        tagType = self.comboboxNewTag.GetStringSelection()

        if tagType != '':
            # Get the parent tag.
            treeItemId = self.treeTags.GetSelection()
            self.treeTags.AppendItem(treeItemId, f'{tagType}: New information')



    def onEditTag(self, event):
        ''' Event handler for the edit tag button click. '''
        wxtag.editTag(self.treeTags, self)



    def onRemoveTag(self, event):
        ''' Event handler for the remove tag button click. '''
        treeItem = self.treeTags.GetSelection()
        if treeItem is None:
            return
        if treeItem == self.treeTags.GetRootItem():
            return
        self.treeTags.Delete(treeItem)



    def populateDialog(self):
        ''' Populate the dialog from the Source. '''
        # Common inputs.
        self.textTitle.SetValue(self.source.title)
        if self.source.date is not None:
            self.textDate.SetValue(self.source.date.toGedCom())
        if self.source.place is not None:
            # self.textPlace.SetValue(self.source.place.toIdentityCheck())
            self.textPlace.SetValue(self.source.place.place)
            if self.source.place.address is not None:
                self.textAddress.SetValue(self.source.place.address)

        # Type specific inputs.
        numNotesToIgnore = 0
        if self.source.type != GedComSourceType.GENERAL:
            numNotesToIgnore = 1

            grid = None
            if self.source.tags is not None:
                for tag in self.source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information

            if grid is not None:
                if self.source.type == GedComSourceType.MARRIAGE_CERTIFICATE:
                    self.textGroReference.SetValue(grid[0][2])

                    self.textGroomName.SetValue(grid[1][1])
                    self.textGroomAge.SetValue(grid[1][3])
                    self.textGroomProfession.SetValue(grid[1][4])
                    self.textGroomResidence.SetValue(grid[1][5])

                    self.textBrideName.SetValue(grid[2][1])
                    self.textBrideAge.SetValue(grid[2][3])
                    self.textBrideProfession.SetValue(grid[2][4])
                    self.textBrideResidence.SetValue(grid[2][5])

                    self.textGroomFatherName.SetValue(grid[3][1])
                    self.textGroomFatherProfession.SetValue(grid[3][3])
                    self.textBrideFatherName.SetValue(grid[4][1])
                    self.textBrideFatherProfession.SetValue(grid[4][3])

                    self.textWitness.SetValue(grid[5][1])
        else:
            # General source.
            self.comboboxType.SetSelection(self.source.type.value - 1)

        # Add the tags to the one and only root.
        root = self.treeTags.AddRoot(self.source.title)
        if self.source.tags is not None:
            for tag in self.source.tags:
                print(tag.type)
                if tag.type == 'NOTE':
                    if numNotesToIgnore == 0:

                        wxtag.addTagToTree(self.treeTags, root, tag)
                    else:
                        print('Ignore note tag')
                        numNotesToIgnore -= 1
                else:
                    wxtag.addTagToTree(self.treeTags, root, tag)
        self.treeTags.Toggle(root)

        # Update the layout.
        self.panel.Layout()



    def writeChanges(self):
        ''' Populate the individual with values from the dialog. '''
        print('writeChanges()')
        # Common inputs.
        self.source.title = self.textTitle.GetValue()
        theDate = self.textDate.GetValue()
        if theDate != '':
            self.source.date = GedComDate(theDate)
        thePlace = self.textPlace.GetValue()
        if thePlace != '':
            self.source.place = GedComPlace()
            self.source.place.place = thePlace
            theAddress = self.textAddress.GetValue()
            if theAddress != '':
                self.source.place.address = theAddress

        # The type specific input may want to edit the tags.
        self.source.tags = None

        # Type specific inputs.
        if self.source.type == GedComSourceType.MARRIAGE_CERTIFICATE:
            tag = GedComTag([f'1 NOTE GRID: GRO Reference: {self.textGroReference.GetValue()}', f'2 CONT Groom: {self.textGroomName.GetValue()}: : {self.textGroomAge.GetValue()}: {self.textGroomProfession.GetValue()}: {self.textGroomResidence.GetValue()}', f'2 CONT Bride: {self.textBrideName.GetValue()}: : {self.textBrideAge.GetValue()}: {self.textBrideProfession.GetValue()}: {self.textBrideResidence.GetValue()}', f'2 CONT Groom\'s Father: {self.textGroomFatherName.GetValue()}: : {self.textGroomFatherProfession.GetValue()}', f'2 CONT Bride\'s Father: {self.textBrideFatherName.GetValue()}: : {self.textBrideFatherProfession.GetValue()}', f'2 CONT Witness: {self.textWitness.GetValue()}'])
            self.source.tags = []
            self.source.tags.append(tag)
        else:
            self.source.type = GedComSourceType(self.comboboxType.GetSelection() + 1)
        self.source.setTitleFromType()

        # Loop through the tags.
        print('Loop through tags')

        root = self.treeTags.GetRootItem()
        item, cookie = self.treeTags.GetFirstChild(root)
        while item.IsOk():
            tag = wxtag.getTagFromTree(self.treeTags, root, item)

            # This is for debuging only.
            if isinstance(tag, GedComTag):
                for line in tag.toGedCom():
                    print(line)

            if self.source.tags is None:
                self.source.tags = []
            self.source.tags.append(tag)

            # Get the next tag.
            item, cookie = self.treeTags.GetNextChild(root, cookie)

        # Update the change record.
        self.gedcom.isDirty = True
        if self.source.change is None:
            self.source.change = GedComChange()
        self.source.change.setNow()



    def editSource(self):
        ''' Show the dialog with an initial source to edit. '''
        # Populate the dialog with the individual settings.
        self.populateDialog()

        # Default function result.
        isResult = False

        # Show the dialog and wait for a response.
        if self.ShowModal() == wx.ID_OK:
            self.writeChanges()
            isResult = True

        # Return the result.
        return isResult
