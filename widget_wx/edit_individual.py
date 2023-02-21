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
import widget_wx.gedcom_tag as wxtag
from gedcom_tag import GedComTag
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
        self.comboboxSex = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=['Male', 'Female'])
        self.comboboxSex.Bind(wx.EVT_SET_FOCUS, self.onFocusGeneral)
        groupDetailsSizer.Add(self.comboboxSex, 0, wx.ALL | wx.ALIGN_LEFT)
        groupDetails.Add(groupDetailsSizer, 0, wx.EXPAND | wx.ALL, 2)
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Tags group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Tags')
        self.treeTags = wx.TreeCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(-1, 150), style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS)
        self.treeTags.Bind(wx.EVT_SET_FOCUS, self.onFocusTree)
        self.treeTags.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelectionChange)
        groupDetails.Add(self.treeTags, 0, wx.ALL | wx.EXPAND, 2)
        panelButtons = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Tag')
        panelButtons.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxNewTag = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=wxtag.getNewTagIndividualOptions())
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

        # Sources group box.
        self.groupSources = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Sources')
        self.listboxSources = wx.ListBox(self.groupSources.GetStaticBox(), wx.ID_ANY)
        self.groupSources.Add(self.listboxSources, 0, wx.ALL | wx.EXPAND, 2)
        boxsizerNewSource = wx.BoxSizer(wx.HORIZONTAL)
        self.comboboxNewSource = wx.ComboBox(self.groupSources.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, choices=[])
        boxsizerNewSource.Add(self.comboboxNewSource, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 2)
        buttonAddSource = wx.Button(self.groupSources.GetStaticBox(), wx.ID_ANY, 'Add')
        buttonAddSource.Bind(wx.EVT_BUTTON, self.onAddSource)
        boxsizerNewSource.Add(buttonAddSource, 0, wx.ALL | wx.ALIGN_LEFT, 2)
        buttonRemoveSource = wx.Button(self.groupSources.GetStaticBox(), wx.ID_ANY, 'Remove')
        buttonRemoveSource.Bind(wx.EVT_BUTTON, self.onRemoveSource)
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
        self.activeSources = self.generalSources
        self.listboxSources.Clear()
        for sourceIdentity in self.generalSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusName(self, event):
        ''' Event handler for name getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('Sources for Name')
        self.activeSources = self.nameSources
        self.listboxSources.Clear()
        for sourceIdentity in self.nameSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusDoB(self, event):
        ''' Event handler for DoB getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('Sources for DoB')
        self.activeSources = self.dobSources
        self.listboxSources.Clear()
        for sourceIdentity in self.dobSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()



    def onFocusDoD(self, event):
        ''' Event handler for DoB getting focus. '''
        self.groupSources.GetStaticBox().SetLabel('Sources for DoD')
        self.activeSources = self.dodSources
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
        treeItem = self.treeTags.GetSelection()
        # Label the sources.
        treeItemText = self.treeTags.GetItemText(treeItem)
        self.groupSources.GetStaticBox().SetLabel(treeItemText)
        # Update the sources.
        self.listboxSources.Clear()
        sources = self.treeTags.GetItemData(treeItem)
        if sources is not None:
            self.activeSources = sources
            for sourceIdentity in sources:
                source = self.gedcom.sources[sourceIdentity]
                self.listboxSources.Append(source.title, source)
        else:
            # Create a sources list.
            print('Create a sources list')
            self.activeSources = []
            self.treeTags.SetItemData(treeItem, self.activeSources)

        # Update the possible child tags.
        if treeItem == self.treeTags.GetRootItem():
            newTagOptions = wxtag.getNewTagIndividualOptions()
        else:
            newTagOptions = wxtag.getNewTagIndividualOptions(self.treeTags, treeItem)
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



    def onAddSource(self, event):
        ''' Event handler for the add source button click. '''
        # Get the new source.
        sourceIndex = self.comboboxNewSource.GetSelection()
        source = self.comboboxNewSource.GetClientData(sourceIndex)
        # Add the source.
        if self.activeSources is not None:
            self.activeSources.append(source.identity)
        self.listboxSources.Append(source.title, source)



    def onRemoveSource(self,event):
        ''' Event handler for the remove source button click. '''
        # Get the source.
        sourceIndex = self.listboxSources.GetSelection()
        if self.activeSources is not None:
            self.activeSources.pop(sourceIndex)
            self.listboxSources.Delete(sourceIndex)



    def populateDialog(self):
        ''' Populate the dialog from the individual. '''
        self.textGivenName.SetValue(self.individual.givenName)
        self.textSurname.SetValue(self.individual.surname)
        if self.individual.birth.date is not None:
            self.textDoB.SetValue(self.individual.birth.date.toGedCom())
        if self.individual.death is not None and self.individual.death.date is not None:
            self.textDoD.SetValue(self.individual.death.date.toGedCom())
        if self.individual.isMale():
            self.comboboxSex.SetSelection(0)
        else:
            self.comboboxSex.SetSelection(1)

        # Add the tags to the one and only root.
        root = self.treeTags.AddRoot(self.individual.getName())
        wxtag.addTagToTree(self.treeTags, root, self.individual.birth)
        if self.individual.death is not None:
            wxtag.addTagToTree(self.treeTags, root, self.individual.death)
        if self.individual.tags is not None:
            for tag in self.individual.tags:
                wxtag.addTagToTree(self.treeTags, root, tag)
        # Add the ToDo to the root as if they were tags.
        if self.individual.todos is not None:
            for todo in self.individual.todos:
                self.treeTags.AppendItem(root, f'ToDo: {todo.rank} {todo.description}')
        self.treeTags.Toggle(root)

        # Initialise the non tag sources.
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
        self.individual.nameSources = self.nameSources
        self.individual.sources = self.generalSources
        birthDate = self.textDoB.GetValue()
        if birthDate != '':
            self.individual.birth.date.parse(birthDate)
            self.individual.birth.date.sources = self.dobSources
            #self.individual.birth.date.sources = []
            #for source in self.dobSources:
            #    self.individual.birth.date.sources.append(source)
        deathDate = self.textDoD.GetValue()
        if deathDate == '':
            self.individual.death = None
        else:
            self.individual.death = GedComTag(['1 DEAT Y', f'2 DATE {deathDate}'])
            self.individual.death.date.sources = self.dodSources
            #for source in self.dodSources:
            #    self.individual.death.date.sources.append(source)
        if self.comboboxSex.GetSelection() == 0:
            self.individual.sex = IndividualSex.MALE
        else:
            self.individual.sex = IndividualSex.FEMALE

        # Loop through the tags.
        print('Loop through tags')
        self.individual.tags = None
        self.individual.todos = None
        root = self.treeTags.GetRootItem()
        item, cookie = self.treeTags.GetFirstChild(root)
        while item.IsOk():
            tag = wxtag.getTagFromTree(self.treeTags, root, item)

            # This is for debuging only.
            for line in tag.toGedCom():
                print(line)

            if tag.type == 'BIRT':
                print('Ignore birth tag')
                if tag.place is not None:
                    self.individual.birth.place = tag.place
                else:
                    self.individual.birth.place = None
            elif tag.type == 'DEAT':
                print('Ignore death tag')
            elif tag.type == '_TODO':
                print('Ignore ToDo')
                if self.individual.todos is None:
                    self.individual.todos = []
                todo = ToDo(self.individual, [f'1 _TODO {tag.information}'])
                self.individual.todos.append(todo)
            else:
                if self.individual.tags is None:
                    self.individual.tags = []
                self.individual.tags.append(tag)

            # Get the next tag.
            item, cookie = self.treeTags.GetNextChild(root, cookie)

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
            self.comboboxNewSource.Append(source.title, source)

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
