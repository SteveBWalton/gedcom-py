# -*- coding: utf-8 -*-

'''
Module to support the editing of individual in gedcom.
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
from gedcom_fact import GedComFact
# from gedcom_date import GedComDate
from gedcom_individual import IndividualSex
from gedcom_source import GedComSource



class EditIndividual(wx.Dialog):
    ''' Class to represent the dialog to edit an individual in gedcom. '''



    def __init__(self, parentWindow):
        '''
        :param WxMainWindow parentWindow: Specify the parent window for this dialog.

        Class constructor the :py:class:`EditIndividual` class.
        Construct the dialog but do not show it.
        Call :py:func:`editIndividual` or :py:func:`editNewIndividual` to actually show the dialog.
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

        ## Details Group box.
        #groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Details')
        #groupDetailsSizer = wx.GridSizer(2, 4, 5, 5)
        ##groupDetails = wx.StaticBox(self.panel, wx.ID_ANY, 'Details')
        ##groupDetailsSizer = wx.StaticBoxSizer(groupDetails, wx.HORIZONTAL)
        #textSeason = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Season')
        #groupDetailsSizer.Add(textSeason, 0, wx.ALL | wx.ALIGN_RIGHT)
        #self._spinCtrlSeason = wx.SpinCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, min=1950, max=2020)
        #groupDetailsSizer.Add(self._spinCtrlSeason, 0, wx.ALL | wx.ALIGN_LEFT)
        #textLocation = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Location')
        #groupDetailsSizer.Add(textLocation, 0, wx.ALL | wx.ALIGN_RIGHT)
        #self._comboxboxLocation = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=[])
        #groupDetailsSizer.Add(self._comboxboxLocation, 0, wx.ALL | wx.ALIGN_LEFT)
        #textDate = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
        #groupDetailsSizer.Add(textDate, 0, wx.ALL | wx.ALIGN_RIGHT)
        #self._datePicker = wx.adv.DatePickerCtrl(groupDetails.GetStaticBox(), wx.ID_ANY)
        #groupDetailsSizer.Add(self._datePicker, 0, wx.ALL | wx.ALIGN_LEFT)
        #textTrack = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Track')
        #groupDetailsSizer.Add(textTrack, 0, wx.ALL | wx.ALIGN_RIGHT)
        #self._comboxboxTrack = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=[])
        #groupDetailsSizer.Add(self._comboxboxTrack, 0, wx.ALL | wx.ALIGN_LEFT)
        #groupDetails.Add(groupDetailsSizer)
        #self.boxsizer.Add(groupDetails)

        ## Results Group box.
        #groupResults = wx.StaticBox(self.panel, wx.ID_ANY, 'Results')
        #self.boxsizer.Add(groupResults)

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
        self.treeFacts = wx.TreeCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(-1, 100))
        groupDetails.Add(self.treeFacts, 0, wx.ALL | wx.EXPAND, 2)
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
        root = self.treeFacts.AddRoot('Facts')
        if self.individual.facts is not None:
            for fact in self.individual.facts:
                self.treeFacts.AppendItem(root, f'{fact.type} {fact.information}')

        self.generalSources = copy.copy(self.individual.sources)
        self.nameSources = copy.copy(self.individual.nameSources)
        self.dobSources = copy.copy(self.individual.birth.date.sources)
        if self.individual.death is None or self.individual.death.date is None:
            self.dodSources = []
        else:
            self.dodSources = copy.copy(self.individual.death.date.sources)
        self.panel.Layout()



    def writeChanges(self):
        ''' Populate the individual with values from the dialog. '''
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



    def editIndividual(self, gedcom, identity):
        '''
        Show the dialog with an initial individual to edit.

        :param Database database: Specify the Database object to fetch the tracks from.
        :param int seasonIndex: Specify the year of the initial race.
        :param int locationIndex: Specify the ID the initial location.
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
        if self.ShowModal() == wx.ID_OK:
            self.writeChanges()
            isResult = True

        # Return the result.
        return isResult
