# -*- coding: utf-8 -*-

'''
Module to support the editing of an individual in gedcom.
This uses the wx library.
'''

# System Libraries.
import wx
import wx.adv
import sqlite3
import datetime
import time
import os
import sys
import copy

# Import my own libraries.
import widget_wx.gedcom_fact as wxfact
from gedcom_fact import GedComFact
from gedcom_individual import IndividualSex
from gedcom_individual import ToDo
from gedcom_source import GedComSource
from gedcom_change import GedComChange



class EditIndividual(wx.Dialog):
    ''' Class to represent the dialog to edit an individual in gedcom. '''



    def __init__(self, parentWindow):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.

        Class constructor the :py:class:`EditIndividual` class.
        Construct the dialog but do not show it.
        Call :py:func:`editIndividual` to actually show the dialog.
        '''
        # Initialise the base class.
        wx.Dialog.__init__(self, parentWindow, title='Edit Individual', style = wx.RESIZE_BORDER)

        # Initialise members.
        self.individual = None
        self.generalSources = []
        self.nameSources = []
        self.dobSources = []
        self.dodSources = []

        # Add a panel to the dialog.
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Add vertical zones to the panel.
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # Details group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Details')
        # wx.GridSizer() all cells are the same size!
        # groupDetailsSizer = wx.GridSizer(3, 4, 5, 5)
        groupDetailsSizer = wx.FlexGridSizer(3, 4, 5, 5)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Surname')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.textSurname = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
        self.textSurname.Bind(wx.EVT_SET_FOCUS, self.onFocusName)
        groupDetailsSizer.Add(self.textSurname, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date of Birth')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.textDoB = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
        self.textDoB.Bind(wx.EVT_SET_FOCUS, self.onFocusDoB)
        groupDetailsSizer.Add(self.textDoB, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Given Names')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.textGivenName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
        self.textGivenName.Bind(wx.EVT_SET_FOCUS, self.onFocusName)
        groupDetailsSizer.Add(self.textGivenName)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date of Death')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.textDoD = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
        self.textDoD.Bind(wx.EVT_SET_FOCUS, self.onFocusDoD)
        groupDetailsSizer.Add(self.textDoD)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboxboxSex = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=['Male', 'Female'])
        self.comboxboxSex.Bind(wx.EVT_SET_FOCUS, self.onFocusGeneral)
        groupDetailsSizer.Add(self.comboxboxSex, 0, wx.ALL | wx.ALIGN_LEFT)
        groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Facts group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Facts')
        self.treeFacts = wx.TreeCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(-1, 150), style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS)
        self.treeFacts.Bind(wx.EVT_SET_FOCUS, self.onFocusTree)
        self.treeFacts.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelectionChange)
        groupDetails.Add(self.treeFacts, 0, wx.ALL | wx.EXPAND, 2)
        panelButtons = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Fact')
        panelButtons.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxFact = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=wxfact.getNewFactIndividualOptions())
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

        # Sources group box.
        self.groupSources = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Sources')
        self.listboxSources = wx.ListBox(self.groupSources.GetStaticBox(), wx.ID_ANY)
        self.groupSources.Add(self.listboxSources, 0, wx.ALL | wx.EXPAND, 2)
        boxsizerNewSource = wx.BoxSizer(wx.HORIZONTAL)
        self.comboxboxNewSource = wx.ComboBox(self.groupSources.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=[])
        boxsizerNewSource.Add(self.comboxboxNewSource, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 2)
        buttonAddSource = wx.Button(self.groupSources.GetStaticBox(), wx.ID_ANY, 'Add')
        boxsizerNewSource.Add(buttonAddSource, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        buttonRemoveSource = wx.Button(self.groupSources.GetStaticBox(), wx.ID_ANY, 'Remove')
        boxsizerNewSource.Add(buttonRemoveSource, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        self.groupSources.Add(boxsizerNewSource, 0, wx.ALL | wx.EXPAND, 2)
        self.boxsizer.Add(self.groupSources, 0, wx.ALL | wx.EXPAND, 2)

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




    def onFocusGeneral(self, event):
        ''' Event handler for name getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('General Sources')
        self.listboxSources.Clear()
        for sourceIdentity in self.generalSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusName(self, event):
        ''' Event handler for name getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('Sources for Name')
        self.listboxSources.Clear()
        for sourceIdentity in self.nameSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusDoB(self, event):
        ''' Event handler for DoB getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('Sources for DoB')
        self.listboxSources.Clear()
        for sourceIdentity in self.dobSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusDoD(self, event):
        ''' Event handler for DoB getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('Sources for DoD')
        self.listboxSources.Clear()
        for sourceIdentity in self.dodSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusTree(self, event):
        ''' Event handler for the tree control getting focus. '''
        self.onTreeSelectionChange(event)



    def onTreeSelectionChange(self, event):
        ''' Event handler for the tree control selection changing. '''
        treeItemId = self.treeFacts.GetSelection()
        # Label the sources.
        treeItemText = self.treeFacts.GetItemText(treeItemId)
        self.groupSources.GetStaticBox().SetLabel(treeItemText)
        # Update the sources.
        self.listboxSources.Clear()
        sources = self.treeFacts.GetItemData(treeItemId)
        if sources is not None:
            for sourceIdentity in sources:
                source = self.gedcom.sources[sourceIdentity]
                self.listboxSources.Append(source.title, source)
        # Update the possible child facts.
        if treeItemId == self.treeFacts.GetRootItem():
            newFactOptions = wxfact.getNewFactIndividualOptions()
        else:
            newFactOptions = wxfact.getNewFactIndividualOptions(treeItemId)
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
        wxfact.editFact(self.treeFacts, self)



    def onRemoveFact(self, event):
        ''' Event handler for the remove fact button click. '''
        treeItem = self.treeFacts.GetSelection()
        if treeItem is None:
            return
        if treeItem == self.treeFacts.GetRootItem():
            return
        self.treeFacts.Delete(treeItem)



    def populateDialog(self):
        ''' Populate the dialog from the individual. '''
        self.textGivenName.SetValue(self.individual.givenName)
        self.textSurname.SetValue(self.individual.surname)
        if self.individual.birth.date is not None:
            self.textDoB.SetValue(self.individual.birth.date.toGedCom())
        if self.individual.death is not None and self.individual.death.date is not None:
            self.textDoD.SetValue(self.individual.death.date.toGedCom())
        if self.individual.isMale():
            self.comboxboxSex.SetSelection(0)
        else:
            self.comboxboxSex.SetSelection(1)

        # Add the facts to the one and only root.
        root = self.treeFacts.AddRoot(self.individual.getName())
        wxfact.addFactToTree(self.treeFacts, root, self.individual.birth)
        if self.individual.death is not None:
            wxfact.addFactToTree(self.treeFacts, root, self.individual.death)
        if self.individual.facts is not None:
            for fact in self.individual.facts:
                wxfact.addFactToTree(self.treeFacts, root, fact)
        # Add the ToDo to the root as if they were facts.
        if self.individual.todos is not None:
            for todo in self.individual.todos:
                self.treeFacts.AppendItem(root, f'ToDo: {todo.rank} {todo.description}')
        self.treeFacts.Toggle(root)

        # Initialise the non fact sources.
        self.generalSources = copy.copy(self.individual.sources)
        self.nameSources = copy.copy(self.individual.nameSources)
        self.dobSources = copy.copy(self.individual.birth.date.sources)
        if self.individual.death is None or self.individual.death.date is None:
            self.dodSources = []
        else:
            self.dodSources = copy.copy(self.individual.death.date.sources)
        # Update the layout.
        self.panel.Layout()



    def writeChanges(self):
        ''' Populate the individual with values from the dialog. '''
        print('writeChanges()')
        self.individual.givenName = self.textGivenName.GetValue()
        self.individual.surname = self.textSurname.GetValue()
        birthDate = self.textDoB.GetValue()
        if birthDate != '':
            self.individual.birth.date.parse(birthDate)
            self.individual.birth.date.sources = []
            for source in self.dobSources:
                self.individual.birth.date.sources.append(source)
        deathDate = self.textDoD.GetValue()
        if deathDate == '':
            self.individual.death = None
        else:
            self.individual.death = GedComFact(['1 DEAT Y', f'2 DATE {deathDate}'])
            for source in self.dodSources:
                self.individual.death.date.sources.append(source)
        if self.comboxboxSex.GetSelection() == 0:
            self.individual.sex = IndividualSex.MALE
        else:
            self.individual.sex = IndividualSex.FEMALE

        # Loop through the facts.
        print('Loop through facts')
        self.individual.facts = None
        self.individual.todos = None
        root = self.treeFacts.GetRootItem()
        item, cookie = self.treeFacts.GetFirstChild(root)
        while item.IsOk():
            fact = wxfact.getFactFromTree(self.treeFacts, root, item)
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
            elif fact.type == '_TODO':
                print('Ignore ToDo')
                if self.individual.todos is None:
                    self.individual.todos = []
                todo = ToDo(self.individual, [f'1 _TODO {fact.information}'])
                self.individual.todos.append(todo)
            else:
                if self.individual.facts is None:
                    self.individual.facts = []
                self.individual.facts.append(fact)

            # Get the next fact.
            item, cookie = self.treeFacts.GetNextChild(root, cookie)

        # Update the change record.
        self.gedcom.isDirty = True
        if self.individual.change is None:
            self.individual.change = GedComChange()
        self.individual.change.setNow()



    def editIndividual(self, gedcom, identity):
        '''
        Show the dialog with an initial individual to edit.

        :param GedCom gedcom: Specify the gedcom that contains this individual.
        :param str identity: Specify the identity of the individual.
        '''
        # Initialise member variables.
        self.gedcom = gedcom
        self.individual = gedcom.individuals[identity]

        # Add sources to combobox in reverse change order.
        sources = []
        for source in gedcom.sources.values():
            sources.append(source)
        sources.sort(key=GedComSource.byChange, reverse=True)
        for source in sources:
            self.comboxboxNewSource.Append(source.title, source)

        # Populate the dialog with the individual settings.
        self.populateDialog()

        # Default function result.
        isResult = False

        # Show the dialog and wait for a response.
        print('ShowModal()')
        if self.ShowModal() == wx.ID_OK:
            print('ID_OK')
            self.writeChanges()
            isResult = True

        # Return the result.
        return isResult
