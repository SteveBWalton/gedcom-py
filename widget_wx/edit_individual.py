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
        groupDetailsSizer = wx.GridSizer(2, 4, 5, 5)
        textGivenName = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Given Names')
        groupDetailsSizer.Add(textGivenName, 0, wx.ALL | wx.ALIGN_RIGHT)
        textSurname = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Surname')
        groupDetailsSizer.Add(textSurname, 0, wx.ALL | wx.ALIGN_RIGHT)
        textSex = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Sex')
        groupDetailsSizer.Add(textSex, 0, wx.ALL | wx.ALIGN_RIGHT)
        textDoB = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date of Birth')
        groupDetailsSizer.Add(textDoB, 0, wx.ALL | wx.ALIGN_RIGHT)
        textDoD = wx.StaticText(groupDetails.GetStaticBox(), wx.ID_ANY, 'Date of Death')
        groupDetailsSizer.Add(textDoD, 0, wx.ALL | wx.ALIGN_RIGHT)
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



    def _AddLink(self, widget):
        ''' Signal handler for the add link button click. '''
        liststoreLinks = self.builder.get_object('liststoreLinks')
        oNewRow = liststoreLinks.append(None)
        liststoreLinks.set(oNewRow, 0, 0, 1, 0, 2, 'wikipedia', 3, 'http://en.wikipedia.org/wiki/')



    def _DeleteLink(self, widget):
        ''' Signal handler for the delete link button click. '''
        # Find the active row.
        treeviewLinks = self.builder.get_object('treeviewLinks')
        oPath, oFocusColumn = treeviewLinks.get_cursor()
        if oPath == None:
            # Nothing is selected.
            return

        # oTuple is passed as a parameter when the row is double clicked.
        liststoreLinks = self.builder.get_object('liststoreLinks')
        oIter = liststoreLinks.get_iter(oPath)

        # Find the ID of the appearance row to delete.
        nDeleteID = liststoreLinks.get_value(oIter, 0)
        # print 'DeleteID {}'.format(nDeleteID)
        self.links_delete.append(nDeleteID)

        # Remove the identified row.
        liststoreLinks.remove(oIter)



    def _LinkLabelEdited(self, widget, nRow, sNewValue):
        ''' Signal handler for the link label changing in the links treeview. '''
        liststoreLinks = self.builder.get_object('liststoreLinks')
        oIter = liststoreLinks.get_iter(nRow)
        liststoreLinks.set(oIter, 1, 1, 2, sNewValue)



    def _LinkUrlEdited(self, widget, nRow, sNewValue):
        ''' Signal handler for the link url changing in the links treeview. '''
        liststoreLinks = self.builder.get_object('liststoreLinks')
        oIter = liststoreLinks.get_iter(nRow)
        liststoreLinks.set(oIter, 1, 1, 3, sNewValue)



    def _DateIconClick(self, widget, primarySecondary, event):
        ''' Signal handler for the date icon click message. '''
        modEntryCalendar.showCalendarPopup(widget,self.dialog)



    def _AddRow(self, widget):
        ''' Signal handler for the 'Add Row' button. '''
        # Add a new row to the end of results liststore.
        liststoreResults = self.builder.get_object('liststoreResults')
        oNewRow = liststoreResults.append()

        # Find the highest place so far.
        nCount = 0
        nMaxPosition = -2
        oIter = liststoreResults.get_iter_first()
        while oIter:
            nPositionID = liststoreResults.get_value(oIter, 0)
            if nPositionID < 63:
                if nPositionID > nMaxPosition:
                    nMaxPosition = nPositionID
            nCount = nCount+1
            oIter = liststoreResults.iter_next(oIter)
        nMaxPosition = (nMaxPosition & 62)+2
        nPositionID = 1 + (nMaxPosition/2)

        # Find the points for this position.
        sSql = "SELECT Pts FROM Points WHERE Season = {} AND PositionID = {}".format(self.year, nPositionID)
        cnDb = sqlite3.connect(self.database.filename)
        oCursor = cnDb.execute(sSql)
        oRow = oCursor.fetchone()
        oCursor.close
        cnDb.close()
        if oRow == None:
            nPoints = 0
        elif oRow[0] == None:
            nPoints = 0
        else:
            nPoints = 10*oRow[0]

        # Insert a default place for this row.
        liststoreResults.set(oNewRow, 0, nMaxPosition, 1, self.database.GetPosition(nMaxPosition), 8, nPoints)

        # Show this row on the window.
        treeviewResults = self.builder.get_object('treeviewResults')
        oPath = (nCount-1,)
        # print 'Path {}'.format(oPath)
        treeviewResults.scroll_to_cell(oPath, None, True, 1, 0)



    def _AddRetRow(self, widget):
        '''
        Signal handler for the Add RET row button.
        Add a new row to the results grid with 'RET' as the intial position.
        '''
        # Add a new row to the end of results liststore.
        liststoreResults = self.builder.get_object('liststoreResults')
        oNewRow = liststoreResults.append()

        # Find the number of rows.
        nCount = 0
        oIter = liststoreResults.get_iter_first()
        while oIter:
            nCount = nCount+1
            oIter = liststoreResults.iter_next(oIter)

        # Insert a default place for this row.
        liststoreResults.set(oNewRow, 0, 64, 1, 'RET', 8, 0)

        # Show this row on the window.
        treeviewResults = self.builder.get_object('treeviewResults')
        oPath = (nCount-1, )
        treeviewResults.scroll_to_cell(oPath, None, True, 1, 0)



    def _SwapRow(self, widget):
        '''
        Signal handler for the Up row button.
        Swap the driver and team with the row below.
        Originally tried to swap with the row above but below was much easier (next function).
        '''
        # Find the active row.
        treeviewResults = self.builder.get_object('treeviewResults')
        oPath, oFocusColumn = treeviewResults.get_cursor()
        if oPath == None:
            # Nothing is selected
            return

        # oTuple is passed as a parameter when the row is double clicked.
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(oPath)
        if oIter == None:
            return

        # Move to next record.
        oIterNext = liststoreResults.iter_next(oIter)
        if oIterNext == None:
            return

        # Get the details.
        nDriverID = liststoreResults.get_value(oIter, 2)
        sDriver = liststoreResults.get_value(oIter, 3)
        nConstructorID = liststoreResults.get_value(oIter, 4)
        sConstructor = liststoreResults.get_value(oIter, 5)
        nEngineID = liststoreResults.get_value(oIter, 6)
        sEngine = liststoreResults.get_value(oIter, 7)
        nQualify = liststoreResults.get_value(oIter, 9)
        nFastestLap = liststoreResults.get_value(oIter, 10)
        nEntrantID = liststoreResults.get_value(oIter, 11)
        sEntrant = liststoreResults.get_value(oIter, 12)
        sChassis = liststoreResults.get_value(oIter, 13)

        # Swap the drivers.
        liststoreResults.set(oIter, 2, liststoreResults.get_value(oIterNext, 2), 3, liststoreResults.get_value(oIterNext, 3), 4, liststoreResults.get_value(oIterNext, 4), 5, liststoreResults.get_value(oIterNext, 5), 6, liststoreResults.get_value(oIterNext, 6), 7, liststoreResults.get_value(oIterNext, 7), 9, liststoreResults.get_value(oIterNext, 9), 10, liststoreResults.get_value(oIterNext, 10), 11, liststoreResults.get_value(oIterNext, 11), 12, liststoreResults.get_value(oIterNext, 12), 13, liststoreResults.get_value(oIterNext, 13))

        liststoreResults.set(oIterNext, 2, nDriverID, 3, sDriver, 4, nConstructorID, 5, sConstructor, 6, nEngineID, 7, sEngine, 9, nQualify, 10, nFastestLap, 11, nEntrantID, 12, sEntrant, 13, sChassis)

        # Move cursor down.
        oPathNext = oPath.next()
        treeviewResults.set_cursor(oPath)



    def _AddDnqRow(self, widget):
        '''
        Signal handler for the Add DNQ row button.
        Add a new row to the results grid with 'DNQ' as the intial position.
        '''
        # Add a new row to the end of results liststore.
        liststoreResults = self.builder.get_object('liststoreResults')
        oNewRow = liststoreResults.append()

        # Find the number of rows.
        nCount = 0
        oIter = liststoreResults.get_iter_first()
        while oIter:
            nCount = nCount+1
            oIter = liststoreResults.iter_next(oIter)

        # Insert a default place for this row.
        liststoreResults.set(oNewRow, 0, 160, 1, 'DNQ', 8, 0)

        # Show this row on the window.
        treeviewResults = self.builder.get_object('treeviewResults')
        oPath = (nCount-1,)
        treeviewResults.scroll_to_cell(oPath, None, True, 1, 0)



    def _DeleteRow(self, widget):
        ''' Signal handler for the 'Delete Row' button. '''
        # Find the active row.
        treeviewResults = self.builder.get_object('treeviewResults')
        oPath, oFocusColumn = treeviewResults.get_cursor()
        if oPath == None:
            # Nothing is selected
            return

        # oTuple is passed as a parameter when the row is double clicked.
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(oPath)

        # Remove the identified row.
        liststoreResults.remove(oIter)



    def Write(self):
        ''' Write the contents of the dialog to the database. '''
        # Get handlers to the liststores.
        liststoreResults = self.builder.get_object('liststoreResults')
        liststorePositions = self.builder.get_object('liststorePositions')
        liststoreDrivers = self.builder.get_object('liststoreDrivers')
        liststoreTeams = self.builder.get_object('liststoreTeams')

        # Open the database.
        cnDb = sqlite3.connect(self.database.filename)

        # Update the race.
        # This may actually be a delete and then an insert

        # The year on the dialog.
        adjustmentSeason = self.builder.get_object('adjustmentSeason')
        nSeason = int(adjustmentSeason.get_value())

        # Location on the dialog.
        comboboxLocation = self.builder.get_object('comboboxLocation')
        liststoreLocations = self.builder.get_object('liststoreLocations')
        oIter = comboboxLocation.get_active_iter()
        nLocationID = liststoreLocations.get_value(oIter, 0)

        # Track.
        comboboxTrack = self.builder.get_object('comboboxTrack')
        liststoreTracks = self.builder.get_object('liststoreTracks')
        oIter = comboboxTrack.get_active_iter()
        nTrackID = liststoreTracks.get_value(oIter, 0)

        # Date.
        entryDate = self.builder.get_object('entryDate')
        sDate = entryDate.get_text()
        RaceDate = datetime.date(*time.strptime(sDate,"%d-%m-%Y")[:3])
        sDate = '{}-{:0=2}-{:0=2}'.format(RaceDate.year,RaceDate.month,RaceDate.day)

        # Url.
        # entryUrl = self.builder.get_object('entryUrl')
        # sUrl = entryUrl.get_text()

        # Comments.
        textviewNotes = self.builder.get_object('textviewNotes')
        oBuffer = textviewNotes.get_buffer()
        oBufferStart = oBuffer.get_iter_at_line_offset(0, 0)
        oBufferEnd = oBuffer.get_end_iter()
        sNotes = oBuffer.get_text(oBufferStart, oBufferEnd, False)

        if self.location_index == -1:
            sSql = "INSERT INTO Races (LocationID, TheYear, TheDate, TrackID, Notes, Url) VALUES ({}, {}, '{}', {}, {}, NULL);".format(nLocationID, nSeason, sDate, nTrackID, self.database.ToDb(sNotes))
        else:
            sSql = "UPDATE Races SET Notes={}, TheDate='{}', TrackID={}, Url=NULL WHERE LocationID={} AND TheYear={};".format(self.database.ToDb(sNotes), sDate, nTrackID, self.location_index, self.year)
        if self.database.debug:
            print(sSql)
        try:
            cnDb.execute(sSql)
        except:
            print('Error')
            print(sSql)
            print(sys.exc_info()[0])

        # Remove the previous results so we can add theses results.
        if self.location_index != -1:
            # sSql = "DELETE FROM Results WHERE LocationID={} AND TheYear={}".format(self.location_index, self.year);
            sSql = "DELETE FROM RESULTS WHERE LOCATION_ID={} AND THE_YEAR={};".format(self.location_index, self.year);
            if self.database.debug:
                print(sSql)
            cnDb.execute(sSql)

        # Loop through the liststore of results.
        aPositions = {}
        oIter = liststoreResults.get_iter_first()
        while oIter:
            nPositionID = liststoreResults.get_value(oIter, 0)
            nDriverID = liststoreResults.get_value(oIter, 2)
            nConstructorID = liststoreResults.get_value(oIter, 4)
            nEngineID = liststoreResults.get_value(oIter, 6)
            nPoints = liststoreResults.get_value(oIter, 8)
            nQualify = liststoreResults.get_value(oIter, 9)
            nEntrantID = liststoreResults.get_value(oIter, 11)
            sChassis = liststoreResults.get_value(oIter, 13)
            # if nQualify==0:
            #    nQualify = 'NULL'
            if liststoreResults.get_value(oIter, 10):
                nFastestLap = 1
            else:
                nFastestLap = 0

            # Check if the position has already been used.
            if nPositionID in aPositions:
                # Use the next position instead.
                aPositions[nPositionID] = aPositions[nPositionID]+1
                nPositionID = aPositions[nPositionID]
            else:
                # Save this position, so that it is not used again.
                aPositions[nPositionID] = nPositionID

            sSql = "INSERT INTO RESULTS (LOCATION_ID, THE_YEAR, FINAL_POS, QUALIFY_POS, FASTEST_LAP, DRIVER_ID, CONSTRUCTOR_ID, ENGINE_ID, PTS, ENTRANT_ID, CHASSIS) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format(nLocationID, nSeason, nPositionID, nQualify, nFastestLap, nDriverID, nConstructorID, nEngineID, nPoints, nEntrantID, self.database.ToDb(sChassis))
            if self.database.debug:
                print(sSql)

            # Execute the command.
            try:
                cnDb.execute(sSql)
            except:
                print('Error')
                print(sSql)
                print(sys.exc_info()[0])

            # Have to commit now, otherwise the following reads will lock on the database.
            cnDb.commit()

            # Check the year range on the driver and 2 teams.
            oDriver = self.database.GetDriver(nDriverID)
            if oDriver == None:
                print("error bad driver {}".format(nDriverID))
            else:
                if oDriver.first_year>self.year:
                    oDriver.first_year = self.year
                    oDriver.Write()
                if oDriver.last_year<self.year:
                    oDriver.last_year = self.year
                    oDriver.Write()

            oConstructor = self.database.GetTeam(nConstructorID)
            if oConstructor == None:
                print("error bad constructor {}".format(nConstructorID))
            else:
                if oConstructor.first_year > self.year:
                    oConstructor.first_year = self.year
                    oConstructor.Write()
                if oConstructor.last_year < self.year:
                    oConstructor.last_year = self.year
                    oConstructor.Write()

            oEngine = self.database.GetTeam(nEngineID)
            if oEngine == None:
                print("error bad engine {}".format(nConstructorID))
            else:
                if oEngine.first_year > self.year:
                    oEngine.first_year = self.year
                    oEngine.Write()
                if oEngine.last_year < self.year:
                    oEngine.last_year = self.year
                    oEngine.Write()

            oEntrant = self.database.GetTeam(nEntrantID)
            if oEntrant != None:
                if oEntrant.first_year > self.year:
                    oEntrant.first_year = self.year
                    oEntrant.Write()
                if oEntrant.last_year < self.year:
                    oEntrant.last_year = self.year
                    oEntrant.Write()

            # Move to next record.
            oIter = liststoreResults.iter_next(oIter)
        cnDb.commit()

        # Update the links.
        liststoreLinks = self.builder.get_object('liststoreLinks')
        oIter = liststoreLinks.get_iter_first()
        while oIter:
            # Check if the row has changed.
            nChanged = liststoreLinks.get_value(oIter, 1)
            if nChanged != 0:
                # Get information for this row in the liststore.
                nID = liststoreLinks.get_value(oIter, 0)
                sLabel = liststoreLinks.get_value(oIter, 2)
                sUrl = liststoreLinks.get_value(oIter, 3)
                if nID == 0:
                    sSql = 'INSERT INTO Links (TYPEID, LINKID, LABEL, URL) VALUES (3, {}, {}, {});'.format(nLocationID + 1000*nSeason, self.database.ToDb(sLabel), self.database.ToDb(sUrl))
                else:
                    sSql = 'UPDATE LINKS SET LABEL = {}, URL = {} WHERE ID = {};'.format(self.database.ToDb(sLabel), self.database.ToDb(sUrl), nID);
                if self.database.debug:
                    print(sSql)
                # Execute the command.
                cnDb.execute(sSql)

            # Move to next record.
            oIter = liststoreLinks.iter_next(oIter)

        for nDeleteID in self.links_delete:
            sSql = 'DELETE FROM LINKS WHERE ID={};'.format(nDeleteID);
            if self.database.debug:
                print(sSql)
            # Execute the command
            cnDb.execute(sSql)

        # Have to commit now, otherwise the following reads will lock on the database.
        cnDb.commit()

        # Close the database.
        cnDb.close()

        # Mark the data as saved.
        self.changed = False



    def _LocationChanged(self, comboboxLocation):
        ''' The signal handler for the location combobox value changing. '''
        # print('Location Changed')
        liststoreLocations = self.builder.get_object('liststoreLocations')
        if len(liststoreLocations) == 0:
            return
        oIter = comboboxLocation.get_active_iter()
        nLocationID = liststoreLocations.get_value(oIter, 0)
        # print 'The new location is {}'.format(nLocationID)

        if nLocationID == -1:
            # Show the dialog for a new location.
            oDialog = dialogEditLocation.dialogEditLocation(self.dialog)
            if oDialog.EditLocation(self.database, None, 2011):
                pass
        elif nLocationID == -2:
            # Populate the location combobox with the complete list of locations.
            self.PopulateLocations(self.location_index)
        else:
            # Update the list of tracks at this location.
            if self.database != None:
                self.PopulateTracks(self.database, nLocationID, 0)



    def _PositionChanged(self, widget, nRow, iterSelected):
        ''' Signal handler for the position value changing in a cell on the grid control. '''
        # Get the selected values from the combobox.
        liststorePositions = self.builder.get_object('liststorePositions')
        nPositionID = liststorePositions.get_value(iterSelected, 0)
        sLabel = liststorePositions.get_value(iterSelected, 1)

        # Find the regular points for this position.
        sSql = "SELECT Pts FROM Points WHERE Season={} AND PositionID={}".format(self.year, 1 + (nPositionID/2))
        cnDb = sqlite3.connect(self.database.filename)
        oCursor = cnDb.execute(sSql)
        oRow = oCursor.fetchone()
        oCursor.close
        cnDb.close()
        if oRow == None:
            nPoints = 0
        elif oRow[0] == None:
            nPoints = 0
        else:
            nPoints = 10*oRow[0]

        # Update the results liststore.
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set(oIter, 0, nPositionID, 1, sLabel, 8, nPoints)
        self.changed = True



    def _DriverChanged(self, widget, nRow, iterSelected):
        ''' Signal handler for the driver changing in a cell on the grid control. '''
        # Get the selected values from the combobox.
        liststoreDrivers = self.builder.get_object('liststoreDrivers')
        nDriverID = liststoreDrivers.get_value(iterSelected, 0)
        sLabel = liststoreDrivers.get_value(iterSelected, 1)

        if nDriverID == -1:
            # All.
            self.PopulateDriverCombo(-1)
            return
        if nDriverID == -3:
            # More...
            self.PopulateDriverCombo(-3)
            return
        if nDriverID == -2:
            # New.
            oDialog = dialogEditDriver.CEditDriver(self.dialog)
            oDialog.EditDriver(self.database, None, self.year)
            self.PopulateDriverCombo(self.year)
            return

        # Store the selection.
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set(oIter, 2, nDriverID, 3, sLabel)

        # Find the race date (to find the driver's previous team).
        entryDate = self.builder.get_object('entryDate')
        sDate = entryDate.get_text()
        RaceDate = datetime.date(*time.strptime(sDate,"%d-%m-%Y")[:3])
        sDate = '{}-{:0=2}-{:0=2}'.format(RaceDate.year, RaceDate.month, RaceDate.day)

        # Find the previous (just before race date) team for this driver.
        sSql = "SELECT CONSTRUCTOR_ID, ENGINE_ID, ENTRANT_ID, CHASSIS FROM RESULTS INNER JOIN Races ON RESULTS.LOCATION_ID = Races.LocationID AND RESULTS.THE_YEAR = Races.TheYear WHERE DRIVER_ID = {} AND Races.TheDate < '{}' ORDER BY Races.TheDate DESC LIMIT 1;".format(nDriverID, sDate)
        cnDb = sqlite3.connect(self.database.filename)
        if self.database.debug:
            print(sSql)
        oCursor = cnDb.execute(sSql)
        oRow = oCursor.fetchone()
        oCursor.close
        cnDb.close()

        # Set the constructor, engine, entrant and chassis same as the last time.
        if oRow != None:
            oConstructor = self.database.GetTeam(oRow[0])
            oEngine = self.database.GetTeam(oRow[1])
            oEntrant = self.database.GetTeam(oRow[2])
            if self.database.debug:
                print('Chassis {}'.format(oRow[3]))
            if oConstructor != None:
                liststoreResults.set(oIter, 4, oRow[0], 5, oConstructor.name)
            if oEngine != None:
                liststoreResults.set(oIter, 6, oRow[1], 7, oEngine.name)
            if oEntrant != None:
                liststoreResults.set(oIter, 11, oRow[2], 12, oEntrant.name)
            liststoreResults.set(oIter, 13, oRow[3] if oRow[3] != None else '')

        self.changed = True



    def _EntrantChanged(self, widget, nRow, iterSelected):
        ''' Signal handler for the entrant in a grid cell changing. '''
        # Get the selected values from the combobox.
        liststoreTeams = self.builder.get_object('liststoreTeams')
        nEntrantID = liststoreTeams.get_value(iterSelected, 0)
        sLabel = liststoreTeams.get_value(iterSelected, 1)

        # Deal with the special codes.
        if nEntrantID == -1:
            # All.
            self.PopulateTeamCombo(-1)
            return;
        if nEntrantID == -3:
            # More.
            self.PopulateTeamCombo(-3)
            return;
        if nEntrantID == -2:
            # New.
            oDialog = dialogEditTeam.dialogEditTeam(self.dialog)
            oDialog.EditTeam(self.database, None, self.year)
            self.PopulateTeamCombo(self.year)
            return

        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set(oIter, 11, nEntrantID, 12, sLabel)
        self.changed = True



    def _ConstructorChanged(self, widget, nRow, iterSelected):
        ''' Signal handler for the contructor in a grid cell changing. '''
        # Get the selected values from the combobox.
        liststoreTeams = self.builder.get_object('liststoreTeams')
        nConstructorID = liststoreTeams.get_value(iterSelected, 0)
        sLabel = liststoreTeams.get_value(iterSelected, 1)

        # Deal with the special codes.
        if nConstructorID == -1:
            # All.
            self.PopulateTeamCombo(-1)
            return;
        if nConstructorID == -3:
            # More.
            self.PopulateTeamCombo(-3)
            return;
        if nConstructorID == -2:
            # New.
            oDialog = dialogEditTeam.dialogEditTeam(self.dialog)
            oDialog.EditTeam(self.database, None, self.year)
            self.PopulateTeamCombo(self.year)
            return

        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set(oIter, 4, nConstructorID, 5, sLabel)
        self.changed = True



    def _EngineChanged(self, widget, nRow, iterSelected):
        ''' Signal handler for the engine in a grid cell changing. '''
        # Get the selected values from the combobox.
        liststoreTeams = self.builder.get_object('liststoreTeams')
        nEngineID = liststoreTeams.get_value(iterSelected, 0)
        sLabel = liststoreTeams.get_value(iterSelected, 1)

        # Deal with the special codes.
        if nEngineID == -1:
            # All.
            self.PopulateTeamCombo(-1)
            return;
        if nEngineID == -3:
            # More.
            self.PopulateTeamCombo(-3)
            return
        if nEngineID == -2:
            # New.
            oDialog = dialogEditTeam.dialogEditTeam(self.dialog)
            oDialog.EditTeam(self.database, None, self.year)
            self.PopulateTeamCombo(self.year)
            return

        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set(oIter, 6, nEngineID, 7, sLabel)
        self.changed = True



    def _PointsChanged(self, widget, nRow, sNewValue):
        ''' Signal handler for the points in cell changing value. '''
        # print("Points Changed Signal")
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set_value(oIter, 8, int(sNewValue))
        self.changed = True



    def _FastLapChanged(self, widget, nRow):
        ''' Signal handler for the fastest lap flag changing value. '''
        bValue = widget.get_active()
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        if bValue:
            liststoreResults.set_value(oIter, 10, False)
        else:
            liststoreResults.set_value(oIter, 10, True)
        self.changed = True



    def _QualifyChanged(self, widget, nRow, sNewValue):
        ''' Signal handler for the qualifying position in cell changing value. '''
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set_value(oIter, 9, int(sNewValue))
        self.changed = True



    def _ChassisChanged(self, widget, nRow, sNewValue):
        ''' Signal handler for the Chassis cell changing value. '''
        liststoreResults = self.builder.get_object('liststoreResults')
        oIter = liststoreResults.get_iter(nRow)
        liststoreResults.set_value(oIter, 13, sNewValue)
        self.changed = True



    def PopulateDriverCombo(self, nYear):
        '''
        Populate the comboboxes with the drivers from the specified years.

        :param int nYear: Specifies the year to populate the drivers around.
        '''
        # Fetch the liststore.
        liststoreDrivers = self.builder.get_object('liststoreDrivers')
        liststoreDrivers.clear()

        # Connect to the database.
        cnDb = sqlite3.connect(self.database.filename)

        # Fetch the list of drivers.
        bSpecialOption = True
        if nYear == -1:
            # Special case. All drivers.
            sSql = 'SELECT DriverID, Name, FirstSeason, LastSeason FROM Drivers ORDER BY Name;'
            bSpecialOption = False
        elif nYear == -3:
            # Special case.  Extra drivers.
            sSql = 'SELECT DriverID, Name, FirstSeason, LastSeason FROM Drivers WHERE FirstSeason<={} AND LastSeason>={} ORDER BY Name;'.format(self.year+7, self.year-7)
        else:
            # Default. Current drivers plus drivers from previous season.
            sSql = 'SELECT DriverID, Name, FirstSeason, LastSeason FROM Drivers WHERE FirstSeason<={} AND LastSeason>={} ORDER BY Name;'.format(self.year, self.year-1)
        # print sSql
        oCursor = cnDb.execute(sSql)
        for oRow in oCursor:
            oNewRow = liststoreDrivers.append()
            sName = oRow[1]
            if oRow[2] == oRow[3]:
                sName += ' (' + str(oRow[2]) + ')'
            else:
                sName += ' (' + str(oRow[2]) + '-' + str(oRow[3]) + ')'
            if oRow[0] == None:
                print('Error ({}) "{}"'.format(oRow[0], sName))
            else:
                liststoreDrivers.set(oNewRow, 0, oRow[0], 1, sName)
        oCursor.close()

        # Add the special buttons.
        if bSpecialOption:
            oNewRow = liststoreDrivers.append()
            liststoreDrivers.set(oNewRow, 0, -1, 1, 'All...')
            oNewRow = liststoreDrivers.append()
            liststoreDrivers.set(oNewRow, 0, -3, 1, 'More...')

        oNewRow = liststoreDrivers.append()
        liststoreDrivers.set(oNewRow, 0, -2, 1, 'New...')

        # Close the database.
        cnDb.close()



    def PopulateTeamCombo(self, nYear):
        '''
        Populate the comboboxes with the teams from the specified years.

        :param int nYear: Specifies the year to populate the teams combobox around.
        '''
        # Fetch the liststore.
        liststoreTeams = self.builder.get_object('liststoreTeams')
        liststoreTeams.clear()

        # Connect to the database.
        cnDb = sqlite3.connect(self.database.filename)

        bSpecialOption = True
        if nYear == -1:
            # All Teams.
            sSql = 'SELECT TeamID, Name FROM Teams ORDER BY Name;'
            bSpecialOption = False
        elif nYear == -3:
            # Special case.  Extra teams.
            sSql = 'SELECT TeamID, Name FROM Teams WHERE FirstSeason<={} AND LastSeason>={} ORDER BY Name;'.format(self.year+10, self.year-10)
        else:
            # Default. Current teams plus teams from previous season.
            sSql = 'SELECT TeamID, Name FROM Teams WHERE FirstSeason<={} AND LastSeason>={} ORDER BY Name;'.format(self.year, self.year-1)
        oCursor = cnDb.execute(sSql)
        for oRow in oCursor:
            oNewRow = liststoreTeams.append()
            liststoreTeams.set(oNewRow, 0, oRow[0], 1, oRow[1])
        oCursor.close

        # Add the special buttons.
        if bSpecialOption:
            oNewRow = liststoreTeams.append()
            liststoreTeams.set(oNewRow, 0, -1, 1, 'All...')
            oNewRow = liststoreTeams.append()
            liststoreTeams.set(oNewRow, 0, -3, 1, 'More...')

        oNewRow = liststoreTeams.append()
        liststoreTeams.set(oNewRow, 0, -2, 1, 'New...')

        # Close the database.
        cnDb.close()



    def PopulateLocations(self, nLocationID):
        '''
        Populate the location combobox with all the locations.

        :param int nLocationID: Specifies the ID of the location to select.
        '''
        if self.database == None:
            return

        liststoreLocations = self.builder.get_object('liststoreLocations')
        liststoreLocations.clear()
        nCount = 0
        Locations = self.database.GetListLocations()
        for nIndex, nID in enumerate(Locations):
            oLocation = self.database.GetLocation(nID)

            # Create a flag image object.
            oCountry = self.database.GetCountry(oLocation.country_index)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.database.flags_directory +'32x20/' + oCountry.flag_filename)

            oNewRow = liststoreLocations.append(None)
            liststoreLocations.set(oNewRow, 0, oLocation.index, 1, oLocation.name, 2, pixbuf)
            if oLocation.index == nLocationID:
                nCount = nIndex
        # Select the track identified by nLocationID.
        comboboxLocation = self.builder.get_object('comboboxLocation')
        comboboxLocation.set_active(nCount)
        # Add a new track option.
        oNewRow = liststoreLocations.append(None)
        liststoreLocations.set(oNewRow, 0, -1, 1, "New Location...")






    def editIndividual(self, gedcom, individual):
        '''
        Show the dialog with an initial individual to edit.

        :param Database database: Specify the Database object to fetch the tracks from.
        :param int seasonIndex: Specify the year of the initial race.
        :param int locationIndex: Specify the ID the initial location.
        '''
        # Default function result.
        isResult = False

        # Show the dialog and wait for a response.
        if self.ShowModal() == wx.ID_OK:
            isResult = True

        return isResult
