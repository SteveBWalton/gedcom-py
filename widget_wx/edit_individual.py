# -*- coding: utf-8 -*-

'''
Module to support the editing of individual in gedcom.
This uses the wx library.
'''

import wx
import wx.adv
import sqlite3
import datetime
import time
import os
import sys

# Import my own libraries.
#import modEntryCalendar
#import dialogEditDriver
#import dialogEditTeam
#import dialogEditLocation



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
        wx.Dialog.__init__(self, parentWindow, title='Edit Individual')

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
        groupDetailsSizer = wx.GridSizer(3, 4, 5, 5)
        labelSurname = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Surname')
        groupDetailsSizer.Add(labelSurname, 0, wx.ALL | wx.ALIGN_RIGHT)
        self.textSurname = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
        groupDetailsSizer.Add(self.textSurname)
        labelDoB = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date of Birth')
        groupDetailsSizer.Add(labelDoB, 0, wx.ALL | wx.ALIGN_RIGHT)
        self.textDoB = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
        groupDetailsSizer.Add(self.textDoB)
        labelGivenName = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Given Names')
        groupDetailsSizer.Add(labelGivenName, 0, wx.ALL | wx.ALIGN_RIGHT)
        self.textGivenName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
        groupDetailsSizer.Add(self.textGivenName)
        labelDoD = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date of Death')
        groupDetailsSizer.Add(labelDoD, 0, wx.ALL | wx.ALIGN_RIGHT)
        self.textDoD = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
        groupDetailsSizer.Add(self.textDoD)
        labelSex = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
        groupDetailsSizer.Add(labelSex, 0, wx.ALL | wx.ALIGN_RIGHT)
        comboxboxSex = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=['Male', 'Female'])
        groupDetailsSizer.Add(comboxboxSex, 0, wx.ALL | wx.ALIGN_LEFT)
        groupDetails.Add(groupDetailsSizer)
        self.boxsizer.Add(groupDetails)

        # Sources group box.
        groupSources = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Sources')
        boxsizerNewSource = wx.BoxSizer(wx.HORIZONTAL)
        comboxboxNewSource = wx.ComboBox(groupSources.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=['One', 'Two', 'Three'])
        boxsizerNewSource.Add(comboxboxNewSource)
        buttonAddSource = wx.Button(groupSources.GetStaticBox(), wx.ID_OK, 'Add')
        boxsizerNewSource.Add(buttonAddSource)
        buttonRemoveSource = wx.Button(groupSources.GetStaticBox(), wx.ID_OK, 'Remove')
        boxsizerNewSource.Add(buttonRemoveSource)
        groupSources.Add(boxsizerNewSource)
        self.boxsizer.Add(groupSources)

        # Links group box.
        groupLinks = wx.StaticBox(self.panel, wx.ID_ANY, 'Links')
        self.boxsizer.Add(groupLinks)

        # OK / Cancel buttons.
        panelOk = wx.Panel(self.panel, wx.ID_ANY)
        boxsizerOk = wx.BoxSizer(wx.HORIZONTAL)
        buttonOk = wx.Button(panelOk, wx.ID_OK, 'OK')
        boxsizerOk.Add(buttonOk)
        buttonCancel = wx.Button(panelOk, wx.ID_CANCEL, 'Cancel')
        boxsizerOk.Add(buttonCancel)
        panelOk.SetSizer(boxsizerOk)
        self.boxsizer.Add(panelOk)

        ## Control section.
        #sizerControl = wx.BoxSizer(wx.HORIZONTAL)
        #buttonCancel = wx.Button(self.panel, wx.ID_OK, 'Cancel')
        #sizerControl.Add(buttonCancel, 0, wx.ALL | wx.ALIGN_RIGHT)
        #buttonOK = wx.Button(self.panel, wx.ID_OK, 'OK')
        #sizerControl.Add(buttonOK, 0, wx.ALL | wx.ALIGN_RIGHT)
        #self.boxsizer.Add(sizerControl, 0, wx.ALL | wx.ALIGN_RIGHT)

        # Finish the panel.
        self.panel.SetSizer(self.boxsizer)
        self.boxsizer.Fit(self)



    def populateDialog(self, individual):
        ''' Populate the dialog from the individual. '''
        self.textGivenName.SetValue(individual.givenName)
        self.textSurname.SetValue(individual.surname)
        if individual.birthDate is not None:
            self.textDoB.SetValue(individual.birthDate.toGedCom())
        if individual.deathDate is not None:
            self.textDoD.SetValue(individual.deathDate.toGedCom())



    def editIndividual(self, gedcom, identity):
        '''
        Show the dialog with an initial individual to edit.

        :param Database database: Specify the Database object to fetch the tracks from.
        :param int seasonIndex: Specify the year of the initial race.
        :param int locationIndex: Specify the ID the initial location.
        '''
        individual = gedcom.individuals[identity]
        self.populateDialog(individual)

        # Default function result.
        isResult = False

        # Show the dialog and wait for a response.
        if self.ShowModal() == wx.ID_OK:
            isResult = True

        return isResult
