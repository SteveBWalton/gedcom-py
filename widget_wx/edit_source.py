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
from gedcom_census import GedComCensus



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

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Registration District')
            groupDetailsSizer.Add(label, pos=(3,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textRegistrationDistrict = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textRegistrationDistrict, pos=(3,1), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'When')
            groupDetailsSizer.Add(label, pos=(4,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textWhen = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(100,-1))
            groupDetailsSizer.Add(self.textWhen, pos=(4,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Where')
            groupDetailsSizer.Add(label, pos=(4,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textWhere = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textWhere, pos=(4,3), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Name')
            groupDetailsSizer.Add(label, pos=(5,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textName, pos=(5,1), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
            groupDetailsSizer.Add(label, pos=(5,3), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textSex = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(75,-1))
            groupDetailsSizer.Add(self.textSex, pos=(5,4), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Mother')
            groupDetailsSizer.Add(label, pos=(6,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textMotherName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textMotherName, pos=(6,1), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            #label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
            #groupDetailsSizer.Add(label, pos=(5,3), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textMotherFormally = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textMotherFormally, pos=(6,4), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Father')
            groupDetailsSizer.Add(label, pos=(7,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textFatherName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textFatherName, pos=(7,1), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            #label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
            #groupDetailsSizer.Add(label, pos=(5,3), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textFatherProfession = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textFatherProfession, pos=(7,4), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Informant')
            groupDetailsSizer.Add(label, pos=(8,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textInformant = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textInformant, pos=(8,1), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            self.textInformantAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(self.textInformantAddress, pos=(8,4), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'When Registed')
            groupDetailsSizer.Add(label, pos=(9,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textWhenRegistered = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(100,-1))
            groupDetailsSizer.Add(self.textWhenRegistered, pos=(9,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'GRO Reference')
            groupDetailsSizer.Add(label, pos=(9,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textGroReference = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textGroReference, pos = (9,3), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

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
            groupDetailsSizer = wx.GridBagSizer(13, 10)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Title')
            groupDetailsSizer.Add(label, pos = (0,0), span = (1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textTitle = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textTitle, pos = (0,1), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date')
            groupDetailsSizer.Add(label, pos=(1,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textDate = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(140,-1))
            groupDetailsSizer.Add(self.textDate, pos=(1,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Place')
            groupDetailsSizer.Add(label, pos=(1,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textPlace = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textPlace, pos = (1,3), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, pos=(2,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textAddress, pos = (2,3), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Registration District')
            groupDetailsSizer.Add(label, pos=(3,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textRegistrationDistrict = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textRegistrationDistrict, pos=(3,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'When')
            groupDetailsSizer.Add(label, pos=(3,4), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textWhenRegistered = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textWhenRegistered, pos=(3,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'When')
            groupDetailsSizer.Add(label, pos=(4,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textWhen = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textWhen, pos=(4,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Where')
            groupDetailsSizer.Add(label, pos=(4,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textWhere = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textWhere, pos=(4,3), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Name')
            groupDetailsSizer.Add(label, pos=(5,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textName, pos=(5,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
            groupDetailsSizer.Add(label, pos=(5,4), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textSex = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(100,-1))
            groupDetailsSizer.Add(self.textSex, pos=(5,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Birth Date')
            groupDetailsSizer.Add(label, pos=(6,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textBirthWhen = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textBirthWhen, pos=(6,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Location')
            groupDetailsSizer.Add(label, pos=(6,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textBirthWhere = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textBirthWhere, pos=(6,3), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Occupation')
            groupDetailsSizer.Add(label, pos=(7,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textOccupation = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textOccupation, pos=(7,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Usual Address')
            groupDetailsSizer.Add(label, pos=(8,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textUsualAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textUsualAddress, pos=(8,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Cause')
            groupDetailsSizer.Add(label, pos=(9,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_TOP, border = 1)
            self.textCause = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,70), style = wx.TE_MULTILINE)
            groupDetailsSizer.Add(self.textCause, pos=(9,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Informant')
            groupDetailsSizer.Add(label, pos=(10,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textInformant = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textInformant, pos=(10,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Description')
            groupDetailsSizer.Add(label, pos=(10,4), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textInformantDescription = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(100,-1))
            groupDetailsSizer.Add(self.textInformantDescription, pos=(10,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Informant Address')
            groupDetailsSizer.Add(label, pos=(11,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textInformantAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textInformantAddress, pos=(11,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'GRO Reference')
            groupDetailsSizer.Add(label, pos=(12,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textGroReference = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(300,-1))
            groupDetailsSizer.Add(self.textGroReference, pos = (12,1), span=(1,3), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

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
            groupDetailsSizer.Add(self.textPlace, pos = (1,3), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Address')
            groupDetailsSizer.Add(label, pos=(2,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 2)
            self.textAddress = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(400,-1))
            groupDetailsSizer.Add(self.textAddress, pos = (2,3), span=(1,4), flag = wx.ALL | wx.ALIGN_LEFT, border = 2)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Series')
            groupDetailsSizer.Add(label, pos=(3,0), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textSeries = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textSeries, pos=(3,1), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Piece')
            groupDetailsSizer.Add(label, pos=(3,2), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textPiece = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textPiece, pos=(3,3), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Folio')
            groupDetailsSizer.Add(label, pos=(3,4), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textFolio = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textFolio, pos=(3,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Page')
            groupDetailsSizer.Add(label, pos=(3,6), span=(1,1), flag = wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            self.textPage = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(self.textPage, pos=(3,7), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)

            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Name')
            groupDetailsSizer.Add(label, pos=(4,0), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Person')
            groupDetailsSizer.Add(label, pos=(4,2), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Relation')
            groupDetailsSizer.Add(label, pos=(4,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Age')
            groupDetailsSizer.Add(label, pos=(4,4), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Occupation')
            groupDetailsSizer.Add(label, pos=(4,6), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)
            label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Born Location')
            groupDetailsSizer.Add(label, pos=(4,8), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, border = 1)

            grid = None
            if self.source.tags is not None:
                for tag in self.source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information

            line = 5
            self.textName = []
            self.comboboxPerson = []
            self.textAge = []
            self.textRelation = []
            self.textOccupation = []
            self.textBorn = []

            if grid is not None:
                for index in range(1, len(grid)):
                    textName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
                    groupDetailsSizer.Add(textName, pos=(line,0), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
                    textName.SetValue(grid[index][0])
                    self.textName.append(textName)

                    # grid[index][1] is person identity.
                    comboboxPerson = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=[])
                    groupDetailsSizer.Add(comboboxPerson, pos=(line,2), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
                    self.comboboxPerson.append(comboboxPerson)

                    textAge = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(75,-1))
                    groupDetailsSizer.Add(textAge, pos=(line,4), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
                    textAge.SetValue(grid[index][2])
                    self.textAge.append(textAge)
                    textRelation = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
                    groupDetailsSizer.Add(textRelation, pos=(line,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
                    textRelation.SetValue(grid[index][3])
                    self.textRelation.append(textRelation)
                    textOccupation = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
                    groupDetailsSizer.Add(textOccupation, pos=(line,6), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
                    textOccupation.SetValue(grid[index][4])
                    self.textOccupation.append(textOccupation)
                    textBorn = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
                    groupDetailsSizer.Add(textBorn, pos=(line,8), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
                    textBorn.SetValue(grid[index][5])
                    self.textBorn.append(textBorn)

                    line += 1

            # Add an extra row for new input.
            textName = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(textName, pos=(line,0), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            self.textName.append(textName)
            comboboxPerson = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=[])
            groupDetailsSizer.Add(comboboxPerson, pos=(line,2), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            self.comboboxPerson.append(comboboxPerson)
            textAge = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(75,-1))
            groupDetailsSizer.Add(textAge, pos=(line,4), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            self.textAge.append(textAge)
            textRelation = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(150,-1))
            groupDetailsSizer.Add(textRelation, pos=(line,5), span=(1,1), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            self.textRelation.append(textRelation)
            textOccupation = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(textOccupation, pos=(line,6), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            self.textOccupation.append(textOccupation)
            textBorn = wx.TextCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(200,-1))
            groupDetailsSizer.Add(textBorn, pos=(line,8), span=(1,2), flag = wx.ALL | wx.ALIGN_LEFT, border = 1)
            self.textBorn.append(textBorn)

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
        self.originalCensusPeople = []
        numNotesToIgnore = 0
        if self.source.type != GedComSourceType.GENERAL:
            numNotesToIgnore = 1

            grid = None
            if self.source.tags is not None:
                for tag in self.source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information

            if grid is not None:
                if self.source.type == GedComSourceType.BIRTH_CERTIFICATE:
                    self.textGroReference.SetValue(grid[0][2])
                    self.textRegistrationDistrict.SetValue(grid[1][1])
                    self.textWhen.SetValue(grid[2][1])
                    self.textWhere.SetValue(grid[2][2])
                    self.textName.SetValue(grid[3][1])
                    self.textSex.SetValue(grid[3][2])
                    self.textMotherName.SetValue(grid[4][1])
                    self.textMotherFormally.SetValue(grid[4][2])
                    self.textFatherName.SetValue(grid[5][1])
                    self.textFatherProfession.SetValue(grid[5][2])
                    self.textInformant.SetValue(grid[6][1])
                    self.textInformantAddress.SetValue(grid[6][2])
                    self.textWhenRegistered.SetValue(grid[7][1])

                elif self.source.type == GedComSourceType.MARRIAGE_CERTIFICATE:
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

                elif self.source.type == GedComSourceType.DEATH_CERTIFICATE:
                    self.textRegistrationDistrict.SetValue(grid[1][1])
                    self.textWhen.SetValue(grid[2][1])
                    self.textWhere.SetValue(grid[3][1])
                    self.textName.SetValue(grid[4][1])
                    self.textSex.SetValue(grid[4][2])
                    self.textBirthWhen.SetValue(grid[5][1])
                    try:
                        self.textBirthWhere.SetValue(grid[5][2])
                    except:
                        pass
                    self.textOccupation.SetValue(grid[6][1])
                    self.textUsualAddress.SetValue(grid[7][1])
                    self.textCause.SetValue(grid[8][1])
                    self.textInformant.SetValue(grid[9][1])
                    self.textInformantDescription.SetValue(grid[9][2])
                    self.textInformantAddress.SetValue(grid[10][1])
                    self.textGroReference.SetValue(grid[0][2])
                    self.textWhenRegistered.SetValue(grid[11][1])

                elif self.source.type == GedComSourceType.CENSUS:
                    # Add the people to the comboboxes.
                    individuals = self.gedcom.individuals.values()
                    for individual in individuals:
                        for combobox in self.comboboxPerson:
                            combobox.Append(individual.toLongString(), individual)

                    # Select the person in the person comboboxes.
                    for personIndex in range(1, len(grid)):
                        if grid[personIndex][1] != '':
                            self.originalCensusPeople.append(grid[personIndex][1])
                            for index in range(len(self.comboboxPerson[personIndex - 1].Items)):
                                individual = self.comboboxPerson[personIndex - 1].GetClientData(index)
                                # print(f'compare \'{grid[personIndex][1]}\' with \'{individual.identity}\'')
                                if grid[personIndex][1] == individual.identity:
                                    self.comboboxPerson[personIndex - 1].SetSelection(index)
                                    break

                    # Populate the reference.
                    self.textSeries.SetValue(grid[0][3])
                    self.textPiece.SetValue(grid[0][5])
                    self.textFolio.SetValue(grid[0][7])
                    self.textPage.SetValue(grid[0][9])

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
        if self.source.type == GedComSourceType.BIRTH_CERTIFICATE:
            tag = GedComTag([f'1 NOTE GRID: GRO Reference: {self.textGroReference.GetValue()}', f'2 CONT Registration District: {self.textRegistrationDistrict.GetValue()}', f'2 CONT When and Where: {self.textWhen.GetValue()}: {self.textWhere.GetValue()}', f'2 CONT Name: {self.textName.GetValue()}: {self.textSex.GetValue()}', f'2 CONT Mother: {self.textMotherName.GetValue()}: {self.textMotherFormally.GetValue()}', f'2 CONT Father: {self.textFatherName.GetValue()}: {self.textFatherProfession.GetValue()}', f'2 CONT Informant: {self.textInformant.GetValue()}: {self.textInformantAddress.GetValue()}', f'2 CONT When Registered: {self.textWhenRegistered.GetValue()}'])
            self.source.tags = []
            self.source.tags.append(tag)
        elif self.source.type == GedComSourceType.MARRIAGE_CERTIFICATE:
            tag = GedComTag([f'1 NOTE GRID: GRO Reference: {self.textGroReference.GetValue()}', f'2 CONT Groom: {self.textGroomName.GetValue()}: : {self.textGroomAge.GetValue()}: {self.textGroomProfession.GetValue()}: {self.textGroomResidence.GetValue()}', f'2 CONT Bride: {self.textBrideName.GetValue()}: : {self.textBrideAge.GetValue()}: {self.textBrideProfession.GetValue()}: {self.textBrideResidence.GetValue()}', f'2 CONT Groom\'s Father: {self.textGroomFatherName.GetValue()}: : {self.textGroomFatherProfession.GetValue()}', f'2 CONT Bride\'s Father: {self.textBrideFatherName.GetValue()}: : {self.textBrideFatherProfession.GetValue()}', f'2 CONT Witness: {self.textWitness.GetValue()}'])
            self.source.tags = []
            self.source.tags.append(tag)
        elif self.source.type == GedComSourceType.DEATH_CERTIFICATE:
            lines = [f'1 NOTE GRID: GRO Reference: {self.textGroReference.GetValue()}', f'2 CONT Registration District: {self.textRegistrationDistrict.GetValue()}', f'2 CONT When: {self.textWhen.GetValue()}', f'2 CONT Where: {self.textWhere.GetValue()}', f'2 CONT Name: {self.textName.GetValue()}: {self.textSex.GetValue()}', f'2 CONT Date & Place of Birth: {self.textBirthWhen.GetValue()}: {self.textBirthWhere.GetValue()}', f'2 CONT Occupation: {self.textOccupation.GetValue()}', f'2 CONT Usual Address: {self.textUsualAddress.GetValue()}']
            cause = self.textCause.GetValue()
            print(cause)
            causeLines = cause.split('\n')
            print(causeLines)
            isFirst = True
            for causeLine in causeLines:
                print(causeLine)
                if isFirst:
                    # lines.append(f'2 CONT Cause of Death: {self.textCause.GetValue()}')
                    lines.append(f'2 CONT Cause of Death: {causeLine}')
                    isFirst = False
                else:
                    lines.append(f'3 CONT {causeLine}')
            lines.append(f'2 CONT Informant: {self.textInformant.GetValue()}: {self.textInformantDescription.GetValue()}')
            lines.append(f'2 CONT Informant Address: {self.textInformantAddress.GetValue()}')
            lines.append(f'2 CONT When Registered: {self.textWhenRegistered.GetValue()}')
            tag = GedComTag(lines)
            self.source.tags = []
            self.source.tags.append(tag)
        elif self.source.type == GedComSourceType.CENSUS:
            # Remove the old cenus information from.
            for identity in self.originalCensusPeople:
                print(f'Remove the census record from {identity}')
                self.removeCensus(identity)

            # Update this source record.
            addCensusPeople = []
            livingWith = []
            lines = [f'1 NOTE GRID: Reference: Series: {self.textSeries.GetValue()}: Piece: {self.textPiece.GetValue()}: Folio: {self.textFolio.GetValue()}: Page: {self.textPage.GetValue()}']
            for index in range(len(self.textName)):
                name = self.textName[index].GetValue()
                if name != '':
                    selectedPerson = self.comboboxPerson[index].GetSelection()
                    if selectedPerson == wx.NOT_FOUND:
                        personIdentity = ''
                    else:
                        individual = self.comboboxPerson[index].GetClientData(selectedPerson)
                        personIdentity = individual.identity
                        addCensusPeople.append((personIdentity, self.textOccupation[index].GetValue()))

                    age = self.textAge[index].GetValue()
                    lines.append(f'2 CONT {name}: {personIdentity}: {age}: {self.textRelation[index].GetValue()}: {self.textOccupation[index].GetValue()}: {self.textBorn[index].GetValue()}')

                    if age != '':
                        livingWithName = f'{name} ({age})'
                    else:
                        livingWithName = f'{name}'
                    livingWith.append((personIdentity, livingWithName))
            tag = GedComTag(lines)
            self.source.tags = []
            self.source.tags.append(tag)

            # Add census records to.
            for identity in addCensusPeople:
                print(f'Add the census record to {identity[0]}')
                self.addCensus(identity[0], identity[1], livingWith)
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



    def addCensus(self, identity, occupation, livingWithPeople):
        ''' Adds a census tag to the individual based on this census source. '''
        individual = self.gedcom.individuals[identity]
        block = []
        block.append('1 CENS')
        if self.source.date is not None:
            block.append(f'2 DATE {self.source.date.toGedCom()}')
        if self.source.place is not None:
            block.extend(self.source.place.toGedCom(2))
        if occupation != '':
            block.append(f'2 OCCU {occupation}')
        isFirst = True
        for livingWith in livingWithPeople:
            if livingWith[0] != individual.identity:
                if isFirst:
                    block.append(f'2 NOTE Living with {livingWith[1]}')
                    isFirst = False
                else:
                    block.append(f'3 CONT {livingWith[1]}')
        block.append(f'2 SOUR @{self.source.identity}@')
        newCensus = GedComCensus(individual, block)
        if individual.census is None:
            individual.census = []
        individual.census.append(newCensus)

        individual.census.sort(key = GedComCensus.byDate)



    def removeCensus(self, identity):
        ''' Removes a census tags from the individual based on this census source. '''
        individual = self.gedcom.individuals[identity]
        if individual.census is None:
            return

        index = 0
        while index < len(individual.census):
            if self.source.identity in individual.census[index].sources:
                individual.census.pop(index)
            else:
                index += 1

