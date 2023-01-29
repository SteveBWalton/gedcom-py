# -*- coding: utf-8 -*-

'''
Module to support the editing of a family in gedcom.
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
# from gedcom_fact import GedComFact
# from gedcom_date import GedComDate
from gedcom_individual import IndividualSex
from gedcom_source import GedComSource



class EditFamily(wx.Dialog):
    ''' Class to represent the dialog to edit a family in gedcom. '''



    def __init__(self, parentWindow):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.

        Class constructor the :py:class:`EditFamily` class.
        Construct the dialog but do not show it.
        Call :py:func:`editFamily` or :py:func:`editNewFamily` to actually show the dialog.
        '''
        # Initialise the base class.
        wx.Dialog.__init__(self, parentWindow, title='Edit Family', style = wx.RESIZE_BORDER) # , size = wx.Size(1000, 1000)

        # This works but better to try and understand layout better.
        # self.SetInitialSize(wx.Size(1000, 600))

        # Initialise members.
        self.family = None
        self.generalSources = []

        # Add a panel to the dialog.
        self.panel = wx.Panel(self, wx.ID_ANY)

        # Add vertical zones to the panel.
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        # Details group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Details')
        # GridSizer all cells are the same size!
        #groupDetailsSizer = wx.GridSizer(1, 4, 5, 5)
        groupDetailsSizer = wx.FlexGridSizer(1, 4, 5, 5)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Husband')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxHusband = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=[])
        groupDetailsSizer.Add(self.comboboxHusband, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Wife')
        groupDetailsSizer.Add(label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxWife = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=[])
        groupDetailsSizer.Add(self.comboboxWife, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Facts group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Facts')
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Children group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Children')
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Sources group box.
        self.groupSources = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Sources')
        self.listboxSources = wx.ListBox(self.groupSources.GetStaticBox(), wx.ID_ANY)
        self.groupSources.Add(self.listboxSources, 0, wx.ALL | wx.EXPAND, 2)
        boxsizerNewSource = wx.BoxSizer(wx.HORIZONTAL)
        self.comboboxNewSource = wx.ComboBox(self.groupSources.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=[])
        boxsizerNewSource.Add(self.comboboxNewSource, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 2)
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



    def populateDialog(self):
        ''' Populate the dialog from the family. '''
        if self.family.husbandIdentity is not None:
            for index in range(len(self.comboboxHusband.Items)):
                individual = self.comboboxHusband.GetClientData(index)
                if individual.identity == self.family.husbandIdentity:
                    self.comboboxHusband.SetSelection(index)
                    break
        if self.family.wifeIdentity is not None:
            for index in range(len(self.comboboxWife.Items)):
                individual = self.comboboxWife.GetClientData(index)
                if individual.identity == self.family.wifeIdentity:
                    self.comboboxWife.SetSelection(index)
                    break

        self.panel.Layout()



    def writeChanges(self):
        ''' Populate the family with values from the dialog. '''
        # Get the husband.
        index = self.comboboxHusband.GetSelection()
        newHusband = self.comboboxHusband.GetClientData(index)
        if newHusband.identity != self.family.husbandIdentity:
            print(f'The husband identity has changed from {self.family.husbandIdentity} to {newHusband.identity}.')
        index = self.comboboxWife.GetSelection()
        newWife = self.comboboxWife.GetClientData(index)
        if newWife.identity != self.family.wifeIdentity:
            print(f'The wife identity has changed from {self.family.wifeIdentity} to {newWife.identity}.')



    def editFamily(self, gedcom, identity):
        '''
        Show the dialog with an initial individual to edit.

        :param Database database: Specify the Database object to fetch the tracks from.
        :param int seasonIndex: Specify the year of the initial race.
        :param int locationIndex: Specify the ID the initial location.
        '''
        # Initialise member variables.
        self.gedcom = gedcom
        self.family = gedcom.families[identity]

        # Add People to the husbands and wives.
        husbands = []
        wives = []
        for individual in gedcom.individuals.values():
            if individual.sex == IndividualSex.MALE:
                husbands.append(individual)
            else:
                wives.append(individual)
        # Sort the people.
        for individual in husbands:
            self.comboboxHusband.Append(individual.toLongString(), individual)
        for individual in wives:
            self.comboboxWife.Append(individual.toLongString(), individual)

        # Add sources to combobox in reverse change order.
        sources = []
        for source in gedcom.sources.values():
            sources.append(source)
        sources.sort(key=GedComSource.byChange, reverse=True)
        for source in sources:
            self.comboboxNewSource.Append(source.title, source)

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
