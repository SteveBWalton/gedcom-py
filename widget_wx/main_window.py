#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to display the main window for the gedcom-py application using wxPython.
This module implements the :py:class:`WxApp` and :py:class:`WxMainWindow` classes.
This is based on the GTK version.
'''

# System libraries for the initial phase.
import sys
import os
import platform
import subprocess
import shutil
import datetime
import wx           # Try package python3-wxpython4 or apt install python3-wxgtk4.0 or python -m pip install wxPython
import wx.html2     # Try package python3-wxpython4-webview or apt install python3-wxgtk-webview4.0

# Application libraries.
import widget_wx.edit_individual
import widget_wx.edit_family
import widget_wx.edit_source
from gedcom_individual import GedComIndividual
from gedcom_family import GedComFamily
from gedcom_source import GedComSource



class WxMainWindow(wx.Frame):
    '''
    :ivar Render render: The :py:class:`~render.Render` object for the Formula One results database.
    :ivar Database database: The :py:class:`~database.Database` object for the Formula One results database.
    :ivar Configuration configuration: The :py:class:`~configuration.Configuration` object for the Formula One results database.
    :ivar YearRange yearRange: The active :py:class:`~year_range.YearRange` object. Adds a year range to the parameters sent to the :py:class:`~render.Render` object.
    :ivar string request: The request target for the current page.
    :ivar string parameters: The parameters passed to the current page.
    :ivar Array history: The page history for the back button.
    :ivar int noEvents: Positive to ignore signals.
    :ivar wx.WebView browser: The WebView object to display the html on the main window.

    Class to represent the wxPython main window for the Formula One results database.
    '''



    def __init__(self, application):
        '''
        :param Application application: The object that represents the gedcom application.

        Class constructor for the :py:class:`WxMainWindow` class.
        '''
        # Initialise base classes.  The 'super' style is more modern but I prefer explicit 'wx.Frame' notation.
        # super(WxMainWindow, self).__init__(None, 1, 'Formula One Results Database')
        wx.Frame.__init__(self, None, 1, 'GedCom Viewer')

        # Report the version number.
        versionNumber = wx.version().replace('.', '·')
        print('wxPython {}.'.format(versionNumber))

        # Intialise the application.
        self.application = application

        # The actions that this class can handle.
        self.actions = {
            'edit_individual'       : self.editIndividual,
            'edit_family'           : self.editFamily,
            'edit_source'           : self.editSource,
        }

        # Build the menu bar.
        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menuFileNew = menuFile.Append(wx.ID_NEW, 'New', 'Start a new gedcom.')
        menuFileOpen = menuFile.Append(wx.ID_OPEN, 'Open...', 'Open an existing gedcom file.')
        menuFileSave = menuFile.Append(wx.ID_SAVE, 'Save', 'Save the gedcom.')
        menuFileSaveAs = menuFile.Append(wx.ID_SAVEAS, 'Save As...', 'Save the gedcom with new file name.')
        menuFile.AppendSeparator()
        menuFileHome = menuFile.Append(wx.ID_HOME, 'Home', 'Goto home page.')
        menuFileIndex = menuFile.Append(wx.ID_ANY, 'Index', 'Goto index page.')
        menuFileBack = menuFile.Append(wx.ID_ANY, 'Back', 'Go back one page.')
        menuFileExit = menuFile.Append(wx.ID_EXIT, 'Quit', 'Quit application.')
        menuBar.Append(menuFile, '&File')
        menuEdit = wx.Menu()
        menuEditEdit = menuEdit.Append(wx.ID_EDIT, 'Edit', 'Edit this record.')
        menuEditAddIndividual = menuEdit.Append(wx.ID_ANY, 'Add New Individual', 'Add a new individual to this gedcom.')
        menuEditAddFamily = menuEdit.Append(wx.ID_ANY, 'Add New Family', 'Add a new family to this gedcom.')
        menuEditAddSource = menuEdit.Append(wx.ID_ANY, 'Add New Source', 'Add a new source to this gedcom.')
        menuBar.Append(menuEdit, '&Edit')
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self._fileNew, menuFileNew)
        self.Bind(wx.EVT_MENU, self._fileOpen, menuFileOpen)
        self.Bind(wx.EVT_MENU, self._fileSave, menuFileSave)
        self.Bind(wx.EVT_MENU, self._fileSaveAs, menuFileSaveAs)
        self.Bind(wx.EVT_MENU, self._fileHome, menuFileHome)
        self.Bind(wx.EVT_MENU, self._fileIndex, menuFileIndex)
        self.Bind(wx.EVT_MENU, self._fileBack, menuFileBack)
        self.Bind(wx.EVT_MENU, self._fileQuit, menuFileExit)
        self.Bind(wx.EVT_MENU, self._editAddIndividual, menuEditAddIndividual)
        self.Bind(wx.EVT_MENU, self._editAddFamily, menuEditAddFamily)
        self.Bind(wx.EVT_MENU, self._editAddSource, menuEditAddSource)

        # Build the toolbar.
        #oToolbar = self.CreateToolBar()
        #toolExit = oToolbar.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('file_exit.png'))
        #oToolbar.Realize()
        #self.Bind(wx.EVT_TOOL, self.OnQuit, toolExit)

        # Build the content controlled by the sizer.
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self._webViewNavigating, self.browser)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((700, 700))

        # The page history for the back button.
        self.history = ['home']

        self.isFullscreen = False

        # Positive to ignore signals.
        self.noEvents = 0

        self.displayCurrentPage()




    def _fileQuit(self, widget):
        ''' Signal handler for the 'File' → 'Quit' menu point. '''
        # Check if the current gedcom is dirty.
        if self.application.gedcom.isDirty:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # Close the main window and hence exit the wxPython loop.
        self.Close()



    def _fileHome(self, widget):
        ''' Signal handler for the 'File' → 'Home' menu point. '''
        self.followLocalLink('home', True)



    def _fileIndex(self, widget):
        ''' Signal handler for the 'File' → 'Index' menu point click. '''
        self.followLocalLink('index', True)



    def _fileBack(self, widget):
        ''' Signal handler for the 'File' → 'Back' menu point. '''
        self.followLocalLink('back', True)



    def _fileOpen(self, widget):
        ''' Signal handler for the 'File' → 'Open' menu point. '''
        # Check if the current gedcom is dirty.
        if self.application.gedcom.isDirty:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # Prompt the user for gedcom file.
        fileName = None
        with wx.FileDialog(self, "Open Gedcom file", wildcard="Gedcom files (*.ged)|*.ged", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                # the user changed their mind.
                return

            # Proceed loading the file chosen by the user
            fileName = fileDialog.GetPath()

        if fileName is not None:
            self.application.gedcom.open(fileName)
            # Display the home page.
            self.followLocalLink('home', True)



    def _fileNew(self, widget):
        ''' Signal handler for the 'File' → 'New' menu item. '''
        # Check if the current gedcom is dirty.
        if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm", wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
            return

        # Start a new gedcom.
        self.application.gedcom.new()

        # Display the home page.
        self.followLocalLink('home', True)



    def _fileSave(self, widget):
        ''' Signal handler for the 'File' → 'Save' menu item. '''
        self.application.gedcom.save()
        # Display the home page.
        self.followLocalLink('home', True)



    def _fileSaveAs(self, widget):
        ''' Signal handler for the 'File' → 'Save As' menu item. '''
        fileName = None
        with wx.FileDialog(self, "Save gedcom file", wildcard="Gedcom files (*.ged)|*.ged|All files (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                # The user changed their mind.
                return

            # Save the selected file name.
            fileName = fileDialog.GetPath()

        if fileName is not None:
            self.application.gedcom.saveAs(fileName)
            # Display the home page.
            self.followLocalLink('home', True)



    def _FilePrint(self, widget):
        ''' Signal handler for the 'File' → 'Print Preview' menu item. '''
        # Save the html to a file.
        fileName = '{}/print.html'.format(self.application.configuration.DIRECTORY)
        outFile = open(fileName, 'w')
        outFile.write(self.application.render.html.toHtml())
        outFile.close()
        if self.application.database.debug:
            print('Created \'{}\'.'.format(fileName))

        # Launch the html with the default viewer.
        subprocess.Popen(['xdg-open', fileName])



    def _EditEdit(self, widget):
        ''' Signal handler for the 'Edit' → 'Edit' menu item and 'Edit' toolbar button. '''
        self.followLocalLink(self.application.render.editTarget, False)



    def _editAddIndividual(self, widget):
        ''' Signal handler for the 'Edit' → 'Add Individual' menu item. '''
        # Add a new individual.
        individual = GedComIndividual()
        GedComIndividual.gedcom.individuals[individual.identity] = individual
        GedComIndividual.gedcom.isDirty = True

        # Display the home page.
        self.followLocalLink('home', True)



    def _editAddFamily(self, widget):
        ''' Signal handler for the 'Edit' → 'Add Family' menu item. '''
        # Add a new family.
        family = GedComFamily()
        GedComFamily.gedcom.families[family.identity] = family
        GedComFamily.gedcom.isDirty = True

        # Display the home page.
        self.followLocalLink('home', True)



    def _editAddSource(self, widget):
        ''' Signal handler for the 'Edit' -> 'Add Source' menu item. '''
        # Add a new source.
        source = GedComSource()
        GedComSource.gedcom.sources[source.identity] = source
        GedComSource.gedcom.isDirty = True
        # Display the home page.
        self.followLocalLink('home', True)



    def _EditCopy(self, widget):
        ''' Signal handler for the 'Edit' → 'Copy' menu item. '''
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.set_text(self.application.render.clipboard_text, -1)


    def _ViewFullscreen(self, widget):
        ''' Signal handler for the 'View' → 'Fullscreen' menu item. '''
        #toolbarMain = self.builder.get_object('toolbarMain')
        #menubarMain = self.builder.get_object('menubarMain')
        if self.isFullscreen:
            self.ShowFullScreen(False)
            #self.window.unfullscreen()
            #toolbarMain.set_visible(True)
            #menubarMain.set_visible(True)
            self.isFullscreen = False
        else:
            self.ShowFullScreen(True)
            #self.window.fullscreen()
            #toolbarMain.set_visible(False)
            #menubarMain.set_visible(False)
            self.isFullscreen = True



    def _ViewPrevious(self, widget):
        ''' Signal handler for the 'View' → 'Previous' menu item. '''
        self.followLocalLink(self.application.render.previous_page, True)



    def _ViewNext(self, widget):
        ''' Signal handler for the 'View' → 'Next' menu item. '''
        self.followLocalLink(self.application.render.next_page, True)



    def _ViewAgeToggled(self, widget):
        ''' Signal handler for the 'View' → 'Show Age' menu item. '''
        if self.application.database.debug:
            print("AgeToggled by "+type(widget).__name__)

        if self.noEvents > 0:
            if self.application.database.debug:
                print("No Events ({}).".format(self.noEvents))
            return

        # No more signals / events.
        self.noEvents += 1

        bActive = widget.get_active()

        if type(widget).__name__ == 'ToggleToolButton':
            # Update the menu.
            menuitemViewAge = self.builder.get_object('menuitemViewAge')
            if menuitemViewAge.get_active() != bActive:
                menuitemViewAge.set_active(bActive)
        elif type(widget).__name__ == 'CheckMenuItem':
            # Update the widget.
            toolbuttonAge = self.builder.get_object('toolbuttonAge')
            if toolbuttonAge.get_active() != bActive:
                toolbuttonAge.set_active(bActive)

        # Update the page.
        self.application.OpenCurrentPage()

        # Events / Signals back on.
        self.noEvents -= 1



    def _ViewDebug(self, widget):
        ''' Signal handler for the 'View' -> 'Debug' menu point toggled event. '''
        self.application.database.debug = widget.get_active()
        if self.application.database.debug:
            # Add the debug stylesheet.
            self.application.render.html.stylesheets.append('file:' + os.path.dirname(os.path.realpath(__file__)) + os.sep + 'debug.css')
            for sheet in self.application.render.html.stylesheets:
                print(sheet)
        else:
            # Remove the debug stylesheet.
            if len(self.application.render.html.stylesheets) == 3:
                del self.application.render.html.stylesheets[2]
        # Update the page.
        self.OpenCurrentPage()



    def _HelpAbout(self, widget):
        ''' Signal handler for the 'Help' → 'About' menu item. '''
        self.followLocalLink('about', False)



    def _webViewNavigating(self, event):
        ''' Signal handler for the navigating event on the wx.html2.WebView control. '''
        # print('event = {}'.format(event))
        # help(event)
        # print('event.GetTarget() = {}'.format(event.GetTarget()))
        # print('event.GetURL() = {}'.format(event.GetURL()))

        uri = event.GetURL()

        # print 'Navigation Request url: ', uri
        if uri.startswith('app:'):
            # Follow the local link.
            event.Veto()
            self.followLocalLink(uri[4:], True)
        # Open Links externally.
        if uri.startswith('http:') or uri.startswith('https:'):
            # Open the specified link with the default handler.  Previously this was fixed as firefox.
            event.Veto()
            subprocess.Popen(['xdg-open', uri])
        return



    def saveDocument(self, fileName):
        '''
        :param string fileName: Specifies the full filename of the file to write.

        Write the current document to the specified file.
        '''
        # Adjust the style sheet to an absolute url
        # sOriginal = self.application.render.html.stylesheets[0]
        # self.application.render.html.stylesheets[0] = 'file://' + os.getcwd() + os.sep +'modelling-print.css'

        # Create the document as a file.
        outFile = open(fileName, 'w')
        outFile.write(self.application.render.html.toHtml())
        outFile.close()
        print('Create "{}"'.format(fileName))

        # Restore the relative url to the style sheet
        # self.application.render.html.stylesheets[0] = sOriginal



    def followLocalLink(self, linkUrl, isAddToHistory):
        '''
        :param string linkUrl: Specify the link to follow.  This is expected to be the link after the 'app:' prefix.
        :param boolean isAddToHistory: Specify true to add the specified link to the history.

        Enact the specified local link.
        Decode the link, update history, update cursor and put :py:func:`~applicaiton.Application.openCurrentPage` in the idle queue.
        This only deals with links of the form 'app:{linkUrl}', ie local links.
        Display chain is :py:func:`followLocalLink` -> :py:func:`~application.Applicaiton.openCurrentPage` -> :py:func:`displayCurrentPage`.
        '''
        if self.application.debug:
            print('wx.mainWindow.followLocalLink("{}")'.format(linkUrl))
        isDecode = True

        # Show the wait cursor.

        # Check for an exit request.
        if linkUrl == 'quit':
            # Close the main window and hence exit the main loop.
            self.Close()

        # Check for a back request.
        if linkUrl == 'back':
            if len(self.history) > 0:
                linkUrl = self.history.pop()
                if len(self.history) > 0:
                    linkUrl = self.history.pop()
                else:
                    linkUrl = 'home'
            else:
                linkUrl = 'home'

        # Check for a control code.
        if linkUrl == 'fullscreen':
            isDecode = False
            self._ViewFullscreen(None)

        # Add this link to the history.
        if linkUrl[0:4] != 'edit':
            if isAddToHistory:
                if len(self.history) > 5:
                    self.history.pop(0)
                self.history.append(linkUrl)
        # print(self.history)

        # Decode the request into action and parameters.
        if isDecode:
            nSplit = linkUrl.find('?')
            if nSplit == -1:
                self.application.request = linkUrl
                self.application.parameters = ''
            else:
                self.application.parameters = linkUrl[nSplit+1:]
                self.application.request = linkUrl[:nSplit]

            if self.application.debug:
                print("\trequest '{}', parameters '{}'".format(self.application.request, self.application.parameters))

        # Call the next function in the display chain.
        self.application.openCurrentPage()




    def displayCurrentPage(self):
        '''
        Display the current content on the window.
        This is mainly the html content in the webview widget but also includes updating the toolbar options.
        This does not reload the page from the render object, use :py:func:`~application.Application.openCurrentPage` for that.
        Display chain is :py:func:`followLocalLink` -> :py:func:`~application.Application.openCurrentPage` -> :py:func:`displayCurrentPage`.
        '''
        if self.application.debug:
            print("wx.mainWindow.displayCurrentPage()")

        # No events / signals until this finishes.
        self.noEvents += 1

        # Display the html content on the wx.html2.WebView control.
        self.browser.SetPage(self.application.render.html.toHtml(), 'file:///')

        # Remove the wait cursor.

        # Enable events / signals again.
        self.noEvents -= 1



    def editIndividual(self, parameters):
        ''' Display the dialog to edit the specified individual. '''
        identity = parameters['id'] if 'id' in parameters else identity

        print(f'Edit {identity}')

        dialog = widget_wx.edit_individual.EditIndividual(self)
        if dialog.editIndividual(self.application.gedcom, identity):
            print(f'Update {identity}')
            self.followLocalLink(f'individual?id={identity}', False)
        else:
            print('Cancel changes.')



    def editFamily(self, parameters):
        ''' Display the dialog to edit the specified family. '''
        identity = parameters['id'] if 'id' in parameters else identity

        print(f'Edit {identity}')

        dialog = widget_wx.edit_family.EditFamily(self)
        if dialog.editFamily(self.application.gedcom, identity):
            print(f'Update {identity}')
            self.followLocalLink(f'family?id={identity}', False)
        else:
            print('Cancel changes.')



    def editSource(self, parameters):
        ''' Display the dialog to edit the specified source. '''
        identity = parameters['id'] if 'id' in parameters else identity

        print(f'Edit {identity}')

        dialog = widget_wx.edit_source.EditSource(self, self.application.gedcom, identity)
        if dialog.editSource():
            print(f'Update {identity}')
            self.followLocalLink(f'source?id={identity}', False)
        else:
            print('Cancel changes.')



class WxApp(wx.App):
    '''
    :ivar WxMainWindow frame: The main window for the application.

    Class to represent the Wx application to the WxMainWindow.
    '''


    def __init__(self, application):
        '''
        :param Application application: The object that represents the gedcom application.
        :param object args: The program arguments.

        Class constructor for the :py:class:`WxApp` object.
        This builds a :py:class:`WxMainWindow` object in the :py:attr:`frame` attribute.
        '''
        # Initialise the base class.
        # wx.App.__init__(self)
        super(WxApp, self).__init__()

        #self.name = 'Hello'
        #self.application = application
        #self.args = args

        # Display the main window.
        self.frame = WxMainWindow(application)
        #self.frame = WxMainWindow(self.application, self.args)
        # self.frame = WxMainWindow(None, None)
        self.frame.Show(True)

        #print('self.name = {}'.format(self.name))



    def runMainLoop(self):
        ''' Run the main wx loop. '''
        self.MainLoop()



    #def OnInit(self):
    #    ''' Class constructor. '''
    #    print('CWxApp.OnInit()')
    #    print('CWxApp.OnInit() Finished.')
    #    return True


