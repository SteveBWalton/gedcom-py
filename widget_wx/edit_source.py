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
from gedcom_change import GedComChange



class EditSource(wx.Dialog):
    ''' Class to represent the dialog to edit a source in gedcom. '''



    def __init__(self, parentWindow):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.

        Class constructor the :py:class:`EditSource` class.
        Construct the dialog but do not show it.
        Call :py:func:`editSource` to actually show the dialog.
        '''
        # Initialise the base class.
        wx.Dialog.__init__(self, parentWindow, title='Edit Source', style = wx.RESIZE_BORDER)

        # Initialise members.
        self.source = None

        # Add a panel to the dialog.
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Add vertical zones to the panel.
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # Details group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Details')
        groupDetailsSizer = wx.FlexGridSizer(4, 2, 5, 5)
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
        groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Facts group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Facts')
        self.treeFacts = wx.TreeCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(-1, 150), style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS)
        self.treeFacts.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelectionChange)
        groupDetails.Add(self.treeFacts, 0, wx.ALL | wx.EXPAND, 2)
        panelButtons = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Fact')
        panelButtons.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxFact = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=wxtag.getNewFactSourceOptions())
        panelButtons.Add(self.comboboxFact)
        buttonAdd = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Add')
        buttonAdd.Bind(wx.EVT_BUTTON, self.onAddFact)
        panelButtons.Add(buttonAdd)
        buttonEdit = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Edit')
        buttonEdit.Bind(wx.EVT_BUTTON, self.onEditFact)
        panelButtons.Add(buttonEdit)
        buttonRemove = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Remove')
        buttonRemove.Bind(wx.EVT_BUTTON, self.onRemoveFact)
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
        treeItem = self.treeFacts.GetSelection()
        # Update the possible child facts.
        if treeItem == self.treeFacts.GetRootItem():
            newFactOptions = wxtag.getNewFactSourceOptions()
        else:
            newFactOptions = wxtag.getNewFactSourceOptions(treeItem)
        self.comboboxFact.Clear()
        for option in newFactOptions:
            self.comboboxFact.Append(option)

        # Update the layout.
        self.panel.Layout()



    def onAddFact(self, event):
        ''' Event handler for the add fact button click. '''
        # Get the fact type.
        factType = self.comboboxFact.GetStringSelection()

        if factType != '':
            # Get the parent fact.
            treeItemId = self.treeFacts.GetSelection()
            self.treeFacts.AppendItem(treeItemId, f'{factType}: New information')



    def onEditFact(self, event):
        ''' Event handler for the edit fact button click. '''
        wxtag.editFact(self.treeFacts, self)



    def onRemoveFact(self, event):
        ''' Event handler for the remove fact button click. '''
        treeItem = self.treeFacts.GetSelection()
        if treeItem is None:
            return
        if treeItem == self.treeFacts.GetRootItem():
            return
        self.treeFacts.Delete(treeItem)



    def populateDialog(self):
        ''' Populate the dialog from the Source. '''
        self.textTitle.SetValue(self.source.title)
        self.comboboxType.SetSelection(self.source.type.value - 1)
        #self.textGivenName.SetValue(self.individual.givenName)
        #self.textSurname.SetValue(self.individual.surname)
        #if self.individual.birth.date is not None:
        #    self.textDoB.SetValue(self.individual.birth.date.toGedCom())
        #if self.individual.death is not None and self.individual.death.date is not None:
        #    self.textDoD.SetValue(self.individual.death.date.toGedCom())
        #if self.individual.isMale():
        #    self.comboxboxSex.SetSelection(0)
        #else:
        #    self.comboxboxSex.SetSelection(1)

        # Add the facts to the one and only root.
        root = self.treeFacts.AddRoot(self.source.title)
        #wxtag.addFactToTree(self.treeFacts, root, self.individual.birth)
        #if self.individual.death is not None:
        #    wxtag.addFactToTree(self.treeFacts, root, self.individual.death)
        if self.source.place is not None:
            wxtag.addFactToTree(self.treeFacts, root, self.source.place)
        if self.source.facts is not None:
            for fact in self.source.facts:
                wxtag.addFactToTree(self.treeFacts, root, fact)
        self.treeFacts.Toggle(root)

        # Update the layout.
        self.panel.Layout()



    def writeChanges(self):
        ''' Populate the individual with values from the dialog. '''
        print('writeChanges()')
        self.source.title = self.textTitle.GetValue()
        self.source.type = GedComSourceType(self.comboboxType.GetSelection() + 1)
        self.source.setTitleFromType()
        #if self.comboxboxSex.GetSelection() == 0:
        #    self.individual.sex = IndividualSex.MALE
        #else:
        #    self.individual.sex = IndividualSex.FEMALE

        # Loop through the facts.
        print('Loop through facts')
        self.source.facts = None
        root = self.treeFacts.GetRootItem()
        item, cookie = self.treeFacts.GetFirstChild(root)
        while item.IsOk():
            fact = wxtag.getFactFromTree(self.treeFacts, root, item)
            if fact is None:
                print('Not expecting this.')

            for line in fact.toGedCom():
                print(line)

            if fact.type == 'BIRT':
                print('Ignore birth fact')
                if fact.place is not None:
                    self.individual.birth.place = fact.place
                else:
                    self.individual.birth.place = None
            elif fact.type == 'DEAT':
                print('Ignore death fact')
            else:
                if self.source.facts is None:
                    self.source.facts = []
                self.source.facts.append(fact)

            # Get the next fact.
            item, cookie = self.treeFacts.GetNextChild(root, cookie)

        # Update the change record.
        self.gedcom.isDirty = True
        if self.source.change is None:
            self.source.change = GedComChange()
        self.source.change.setNow()



    def editSource(self, gedcom, identity):
        '''
        Show the dialog with an initial source to edit.

        :param Database database: Specify the Database object to fetch the tracks from.
        :param GedCom gedcom: Specify the gedcom that contains this source.
        :param str identity: Specify the identity the source.
        '''
        # Initialise member variables.
        self.gedcom = gedcom
        self.source = gedcom.sources[identity]

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
