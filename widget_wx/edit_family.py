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
from gedcom_individual import GedComIndividual, IdentitySources, IndividualSex
from gedcom_source import GedComSource
import widget_wx.gedcom_tag as wxtag
from gedcom_change import GedComChange



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

        # Children group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Children')
        self.listboxChildren = wx.ListBox(groupDetails.GetStaticBox(), wx.ID_ANY)
        groupDetails.Add(self.listboxChildren, 0, wx.ALL | wx.EXPAND, 2)
        panelButtons = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Child')
        panelButtons.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxChild = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1))
        panelButtons.Add(self.comboboxChild)
        buttonAdd = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Add')
        buttonAdd.Bind(wx.EVT_BUTTON, self.onAddChild)
        panelButtons.Add(buttonAdd)
        buttonDelete = wx.Button(groupDetails.GetStaticBox(), wx.ID_ANY, 'Remove')
        buttonDelete.Bind(wx.EVT_BUTTON, self.onRemoveChild)
        panelButtons.Add(buttonDelete)
        groupDetails.Add(panelButtons)
        self.boxsizer.Add(groupDetails, 0, wx.EXPAND | wx.ALL, 2)

        # Tags group box.
        groupDetails = wx.StaticBoxSizer(wx.VERTICAL, self.panel, 'Tags')
        self.treeTags = wx.TreeCtrl(groupDetails.GetStaticBox(), wx.ID_ANY, size=(-1, 100), style = wx.TR_HAS_BUTTONS) # wx.TR_HIDE_ROOT
        self.treeTags.Bind(wx.EVT_SET_FOCUS, self.onFocusTree)
        self.treeTags.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelectionChange)
        groupDetails.Add(self.treeTags, 0, wx.ALL | wx.EXPAND, 2)
        panelButtons = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Tag')
        panelButtons.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.comboboxNewTag = wx.ComboBox(groupDetails.GetStaticBox(), wx.ID_ANY, style=wx.CB_READONLY, size=(250,-1), choices=wxtag.getNewTagFamilyOptions())
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
        self.listboxSources.Clear()
        for sourceIdentity in self.generalSources:
            source = self.gedcom.sources[sourceIdentity]
            self.listboxSources.Append(source.title, source)
        self.panel.Layout()










    def onAddChild(self, event):
        ''' Event handler for the add child button. '''
        # Find the selected child.
        childIndex = self.comboboxChild.GetSelection()
        child = self.comboboxChild.GetClientData(childIndex)
        # Add the child.
        self.listboxChildren.Append(child.toLongString(), child)



    def onRemoveChild(self, event):
        ''' Event handler for the remove child button. '''
        childIndex = self.listboxChildren.GetSelection()
        self.listboxChildren.Delete(childIndex)



    def onAddTag(self, event):
        ''' Event handler for the add tag button click. '''
        # Get the tag type.
        tagType = self.comboboxNewTag.GetStringSelection()

        if tagType != '':
            # Get the parent tag.
            treeItem = self.treeTags.GetSelection()
            self.treeTags.AppendItem(treeItem, f'{tagType}: New information')



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
            newTagOptions = wxtag.getNewTagFamilyOptions()
        else:
            newTagOptions = wxtag.getNewTagFamilyOptions(self.treeTags, treeItem)
        self.comboboxNewTag.Clear()
        for option in newTagOptions:
            self.comboboxNewTag.Append(option)

        # Update the layout.
        self.panel.Layout()



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
        ''' Populate the dialog from the family. '''
        # Add People to the husbands and wives.
        husbands = []
        wives = []
        for individual in self.gedcom.individuals.values():
            if individual.sex == IndividualSex.MALE:
                husbands.append(individual)
            else:
                wives.append(individual)
        # Sort the people.
        # Add the people to the comboboxes.
        for individual in husbands:
            self.comboboxHusband.Append(individual.toLongString(), individual)
        for individual in wives:
            self.comboboxWife.Append(individual.toLongString(), individual)

        # Add sources to combobox in reverse change order.
        sources = []
        for source in self.gedcom.sources.values():
            sources.append(source)
        sources.sort(key=GedComSource.byChange, reverse=True)
        for source in sources:
            self.comboboxNewSource.Append(source.title, source)

        # Guess a range for the possible children.
        childStartDate = datetime.date(1600, 1, 1)
        childEndDate = datetime.date.today()

        # Populate the actual husband and wife.
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
            mother = self.gedcom.individuals[self.family.wifeIdentity]
            childStartDate = datetime.date(mother.birth.date.theDate.year + 16, 1, 1)
            childEndDate = datetime.date(mother.birth.date.theDate.year + 50, 12, 31)

        # Add the childrem.
        for childIdentity in self.family.childrenIdentities:
            child = self.gedcom.individuals[childIdentity]
            self.listboxChildren.Append(child.toLongString(), child)

        # Add the possible children.
        for individual in self.gedcom.individuals.values():
            if individual.birth.date.theDate >= childStartDate and individual.birth.date.theDate <= childEndDate:
                self.comboboxChild.Append(individual.toLongString(), individual)

        # Add the tags to the one and only root.
        root = self.treeTags.AddRoot(self.family.getName())
        if self.family.marriage is not None:
            wxtag.addTagToTree(self.treeTags, root, self.family.marriage)
        if self.family.divorce is not None:
            wxtag.addTagToTree(self.treeTags, root, self.family.divorce)
        self.treeTags.Toggle(root)

        self.panel.Layout()



    def writeChanges(self):
        ''' Populate the family with values from the dialog. '''
        # Get the husband.
        index = self.comboboxHusband.GetSelection()
        if index >= 0:
            newHusband = self.comboboxHusband.GetClientData(index)
            if newHusband.identity != self.family.husbandIdentity:
                print(f'The husband identity has changed from {self.family.husbandIdentity} to {newHusband.identity}.')
                # Remove the family from the old husband.
                if self.family.husbandIdentity is not None:
                    husband = GedComIndividual.gedcom.individuals[self.family.husbandIdentity]
                    for spouse in husband.familyIdentities:
                        if spouse.identity == self.family.identity:
                            print('Remove')
                            husband.familyIdentities.remove(spouse)
                # Add the family to the new husband.
                if newHusband.identity is not None:
                    husband = GedComIndividual.gedcom.individuals[newHusband.identity]
                    husband.familyIdentities.append(IdentitySources(self.family.identity))
                    self.family.husbandIdentity = newHusband.identity
        # Get the wife.
        index = self.comboboxWife.GetSelection()
        if index >= 0:
            newWife = self.comboboxWife.GetClientData(index)
            if newWife.identity != self.family.wifeIdentity:
                print(f'The wife identity has changed from {self.family.wifeIdentity} to {newWife.identity}.')
                # Remove the family from the old wife.
                if self.family.wifeIdentity is not None:
                    wife = GedComIndividual.gedcom.individuals[self.family.wifeIdentity]
                    for spouse in wife.familyIdentities:
                        if spouse.identity == self.family.identity:
                            wife.familyIdentities.remove(spouse)
                # Add the family to the new wife.
                if newWife.identity is not None:
                    wife = GedComIndividual.gedcom.individuals[newWife.identity]
                    wife.familyIdentities.append(IdentitySources([f'0 FAMS @{self.family.identity}@', '1 ignore ignore']))
                    self.family.wifeIdentity = newWife.identity

        # Deal with the children.
        newIdentities = []
        for index in range(self.listboxChildren.GetCount()):
            child = self.listboxChildren.GetClientData(index)
            newIdentities.append(child.identity)
        for identity in self.family.childrenIdentities:
            if identity in newIdentities:
                # Nothing to do.
                pass
            else:
                print(f'Remove{identity}')
                child = self.gedcom.individuals[identity]
                child.parentFamilyIdentity = None
        for identity in newIdentities:
            if identity in self.family.childrenIdentities:
                # Nothing to do.
                pass
            else:
                print(f'Add {child.toLongString()}')
                child = self.gedcom.individuals[identity]
                child.parentFamilyIdentity = self.family.identity
        self.family.childrenIdentities = newIdentities

        # Loop through the tagss.
        print('Loop through tags')
        root = self.treeTags.GetRootItem()
        item, cookie = self.treeTags.GetFirstChild(root)
        while item.IsOk():
            tag = wxtag.getTagFromTree(self.treeTags, root, item)

            if tag.type == 'MARR':
                self.family.marriage = tag
            elif tag.type == 'DIV':
                self.family.divorce = tag
            else:
                print(f'Can not deal with \'{tag.type}\'')

            # Get the next tag.
            item, cookie = self.treeTags.GetNextChild(root, cookie)

        # Update the change record.
        self.gedcom.isDirty = True
        if self.family.change is None:
            self.family.change = GedComChange()
        self.family.change.setNow()



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
