# -*- coding: utf-8 -*-

'''
Module to render pages for the gedcom-py program.
This module implements the :py:class:`Render` class.
'''

# System libraries.
# import sys
import datetime
import time
import html

# The program libraries.
import walton.html
import walton.toolbar
from place import Place, PlaceType
from gedcom_individual import GedComIndividual
from gedcom_family import GedComFamily
from gedcom_source import GedComSource
from gedcom_media import GedComMedia



def firstCap(text):
    ''' Returns the text with the first character capitalised. '''
    return text[:1].upper() + text[1:]



def toDoRank(todo):
    ''' Function to rank ToDo items. '''
    return todo.rank



class Render(walton.toolbar.IToolbar):
    ''' Class to render the output from the Formula One results database.
    :ivar Dictionary action: The requests and coresponding fuctions that this class can handle.

    This class inherits from the :py:class:`~walton.toolbar.IToolbar` base class.
    '''



    def __init__(self, application):
        '''
        :param Database database: Specifies the :py:class:`~modDatabase.Database` connection to a database.

        Class constructor for the :py:class:`Render` object.
        '''
        # Base class constructors.
        walton.toolbar.IToolbar.__init__(self)

        # Store the parameters.
        self.application = application
        # Create an Html object.
        self.html = walton.html.Html()

        # Initialise page flags.
        self.editTarget = None
        self.previousPage = None
        self.nextPage = None
        self.showAge = False
        self.levels = None
        self.yearsSelect = False
        self.countrySelect = False
        self.tournamentSelect = False
        self.clipboardText = None
        self.host = 'app:'

        # Define the actions this module can handle and the function to handle the action.
        self.actions = {
            'home'              : self.showHome,
            'index'             : self.showIndex,
            'about'             : self.showAbout,
            'individual'        : self.showIndividual,
            'family'            : self.showFamily,
            'source'            : self.showSource,
            'media'             : self.showMedia,
            'todo'              : self.showToDo,
            'all'               : self.showAll,
            'all_places'        : self.showAllPlaces,
            'place'             : self.showPlace,
        }



    def showAbout(self, _paramtersDictionary):
        ''' Render the about page on the :py:class:`Html` object. '''
        # Clear the html object.
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False)

        self.html.addLine("<h1>About Gedcom Python</h1>")
        self.html.addLine("<p>by Steven Walton 2022-2023</p>")



    def showHome(self, parameters):
        ''' Render the home page. '''
        #if self.application.gedcom.defaultIdentity is not None:
        #    self.showIndividual({'person': self.application.gedcom.defaultIdentity})
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine('<h1>Home</h1>')

        if self.application.gedcom.isDirty:
            self.html.addLine(f'<p>Gedcom \'{self.application.gedcom.fileName}\' needs saving.</p>')
        else:
            self.html.addLine(f'<p>Gedcom \'{self.application.gedcom.fileName}\'.</p>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Individuals</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        count = 0
        individuals = []
        individual = None
        for individual in self.application.gedcom.individuals.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.identity}</a></td>')
                self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
                self.html.addLine('</tr>')
            individuals.append(individual)
        if individual is not None:
            self.html.add('<td>Last</td>')
            self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.identity}</a></td>')
            self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
            self.html.addLine('</tr>')

        # Recent.
        individuals.sort(key=GedComIndividual.byChange, reverse=True)
        for index in range(10):
            if index < len(individuals):
                individual = individuals[index]
                self.html.add('<tr>')
                self.html.add(f'<td>Recent {index + 1}</td>')
                self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.identity}</a></td>')
                self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
                self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are <a href="app:all">{len(individuals)} individuals</a> in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Families</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        families = []
        family = None
        for family in self.application.gedcom.families.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td><a href="app:family?id={family.identity}">{family.identity}</a></td>')
                self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
                self.html.addLine('</tr>')
            families.append(family)
        if family is not None:
            self.html.add('<tr>')
            self.html.add('<td>Last</td>')
            self.html.add(f'<td><a href="app:family?id={family.identity}">{family.identity}</a></td>')
            self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
            self.html.addLine('</tr>')

        # Recent.
        families.sort(key=GedComFamily.byChange, reverse=True)
        for index in range(10):
            if index < len(families):
                family = families[index]
                self.html.add('<tr>')
                self.html.add(f'<td>Recent {index + 1}</td>')
                self.html.add(f'<td><a href="app:family?id={family.identity}">{family.identity}</a></td>')
                self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
                self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are <a href="app:all">{len(families)} families</a> in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Sources</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        sources = []
        source = None
        for source in self.application.gedcom.sources.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td><a href="app:source?id={source.identity}">{source.identity}</a></td>')
                self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
                self.html.addLine('</tr>')
                self.html.add('<tr>')
            sources.append(source)
        if source is not None:
            self.html.add('<td>Last</td>')
            self.html.add(f'<td><a href="app:source?id={source.identity}">{source.identity}</a></td>')
            self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
            self.html.addLine('</tr>')

        # Recent.
        sources.sort(key=GedComSource.byChange, reverse=True)
        for index in range(10):
            if index < len(sources):
                source = sources[index]
                self.html.add('<tr>')
                self.html.add(f'<td>Recent {index + 1}</td>')
                self.html.add(f'<td><a href="app:source?id={source.identity}">{source.identity}</a></td>')
                self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
                self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are <a href="app:all">{len(sources)} sources</a> in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Media</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        mediaObjects = []
        media = None
        for media in self.application.gedcom.media.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td><a href="app:media?id={media.identity}">{media.identity}</a></td>')
                self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
                self.html.addLine('</tr>')
                self.html.add('<tr>')
            mediaObjects.append(media)
        if media is not None:
            self.html.add('<td>Last</td>')
            self.html.add(f'<td><a href="app:media?id={media.identity}">{media.identity}</a></td>')
            self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
            self.html.addLine('</tr>')

        # Recent.
        mediaObjects.sort(key=GedComMedia.byChange, reverse=True)
        for index in range(10):
            if index < len(mediaObjects):
                media = mediaObjects[index]
                self.html.add('<tr>')
                self.html.add(f'<td>Recent {index + 1}</td>')
                self.html.add(f'<td><a href="app:media?id={media.identity}">{media.identity}</a></td>')
                self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
                self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are <a href="app:all">{len(mediaObjects)} media</a> in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.addLine(f'<p>There are <a href="app:all_places">{len(Place.allPlaces)} places</a> in this gedcom.</p>')




    def showIndex(self, _parameters):
        ''' Render the index page. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)

        self.html.addLine('<h1>Index</h1>')
        self.html.addLine('<ul>')
        self.html.addLine('<li><a href="app:home">Home</a></li>')
        self.html.addLine('<li><a href="app:todo">ToDos</a></li>')
        self.html.addLine('<li><a href="app:all">All Elements</a></li>')
        self.html.addLine('<li><a href="app:all_places">All Places</a></li>')
        self.html.addLine('<li><a href="app:about">About</a></li>')
        self.html.addLine('</ul>')



    def addLocalSource(self, localSources, source):
        ''' Add the specified source to the local sources. '''
        if not source in localSources:
            localSources.append(source)
        return chr(ord('A') + localSources.index(source))



    def displayLocalSources(self, localSources):
        ''' Display the local sources in a table. '''
        if len(localSources) == 0:
            return

        self.html.addLine('<table class="reference">')
        index = 0
        for sourceIdentity in localSources:
            self.html.add(f'<tr><td style="text-align: center;">{chr(ord("A") + index)}</td><td>')
            source = self.application.gedcom.sources[sourceIdentity]
            self.html.add(f'<a href="app:source?id={sourceIdentity}">{source.title}</a>')
            self.html.addLine('</td></tr>')
            index += 1
        self.html.addLine('</table>')



    def drawIndividual(self, identity, x, y):
        ''' Draw the specified individual at the specified location. '''
        individual = self.application.gedcom.individuals[identity]

        # Draw the container.
        self.html.addLine(f'<a href="app:individual?person={individual.identity}">')
        if individual.isMale():
            self.html.addLine(f'<rect x="{x}" y="{y}" width="150" height="50" fill="lightskyblue"/>')
        else:
            self.html.addLine(f'<rect x="{x}" y="{y}" width="150" height="50" rx="15" fill="lightpink" />')
        self.html.addLine('</a>')

        # Draw the name.
        self.html.addLine(f'<text font-size="8pt" text-anchor="middle" x="{x+75}" y="{y+12}">{individual.getName()}</text>')

        # Draw the information.
        if individual.birth.date is not None:
            self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+25}">b. {individual.birth.date.toShortString()}</text>')
        if individual.birth.place is not None:
            self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+35}">b. {individual.birth.place.toShortString()}</text>')
        if individual.death is not None:
            if individual.death.date is not None:
                self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+45}">d. {individual.death.date.toShortString()} ({individual.getYears(individual.death.date)})</text>')
            else:
                self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+45}">d. Yes</text>')
        elif individual.birth.date is not None:
            years = individual.getYears()
            if years <= 100:
                self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+45}">age {years}</text>')



    def drawFamilyTree(self, identity):
        ''' Draw a small tree for the specified family. '''
        # Find the family.
        family = self.application.gedcom.families[identity]

        width = 345
        if len(family.childrenIdentities) > 2:
            width = 5 + 170 * len(family.childrenIdentities)

        # Draw the people.
        self.html.addLine(f'<svg style="vertical-align: top; border: 1px solid black; width: {width}px; height: 130px; background-color: white;" viewBox="0 0 {width} 130" xmlns="http://www.w3.org/2000/svg" version="1.1">')

        x = 5
        y = 5
        if family.husbandIdentity is not None:
            self.drawIndividual(family.husbandIdentity, x, y)
            x += 170
        if family.wifeIdentity is not None:
            self.drawIndividual(family.wifeIdentity, x, y)
            x += 170

        x = 5
        y += 70
        for childIdentity in family.childrenIdentities:
            self.drawIndividual(childIdentity, x, y)
            x += 170

        # Close the diagram.
        self.html.addLine('</svg>')



    def drawIndividualTree(self, identity):
        ''' Draw a small tree for the specified individual. '''

        # Setup a grid to add people to.
        rows = [ [], [], [], [] ]

        # Add this person to the second row.
        mainPerson = self.application.gedcom.individuals[identity]
        rows[2].append((identity, 10))

        # Family details (add partner next to person).
        individual = self.application.gedcom.individuals[identity]
        familyCount = 1
        insertPoint = 0
        for familyIdentity in individual.familyIdentities:
            family = self.application.gedcom.families[familyIdentity.identity]
            if family.wifeIdentity is not None:
                if family.wifeIdentity != identity:
                    rows[2].append((family.wifeIdentity, familyCount))
            if family.husbandIdentity is not None:
                if family.husbandIdentity != identity:
                    rows[2].insert(insertPoint, (family.husbandIdentity, familyCount))
                    insertPoint += 1

            for childIdentity in family.childrenIdentities:
                rows[3].append((childIdentity, 10 * familyCount))

            familyCount += 1

        # Siblings.
        siblings = individual.getSiblings()
        insertPoint = 0
        for siblingIdentity in siblings:
            sibling = self.application.gedcom.individuals[siblingIdentity]
            if sibling.parentFamilyIdentity == individual.parentFamilyIdentity:
                code = 10
            else:
                code = 0
            if sibling.birth.date < mainPerson.birth.date:
                # print(f'{sibling.getName()} < {mainPerson.getName()}')
                rows[2].insert(insertPoint, (siblingIdentity, code))
                insertPoint += 1
            else:
                # print(f'{sibling.getName()} > {mainPerson.getName()}')
                rows[2].append((siblingIdentity, code))

        # Parents family.
        if individual.parentFamilyIdentity is not None:
            parentFamily = self.application.gedcom.families[individual.parentFamilyIdentity]
            connectionCode = 10
            if parentFamily.husbandIdentity is not None:
                father = self.application.gedcom.individuals[parentFamily.husbandIdentity]
                if father.parentFamilyIdentity is not None:
                    rows[1].append((parentFamily.husbandIdentity, connectionCode + 1))
                    connectionCode += 10
                    fatherFamily = self.application.gedcom.families[father.parentFamilyIdentity]
                    if fatherFamily.husbandIdentity is not None:
                        rows[0].append((fatherFamily.husbandIdentity, 1))
                    if fatherFamily.wifeIdentity is not None:
                        rows[0].append((fatherFamily.wifeIdentity, 0))
                else:
                    rows[1].append((parentFamily.husbandIdentity, 1))
            if parentFamily.wifeIdentity is not None:
                mother = self.application.gedcom.individuals[parentFamily.wifeIdentity]
                if mother.parentFamilyIdentity is not None:
                    rows[1].append((parentFamily.wifeIdentity, connectionCode + 1))
                    motherFamily = self.application.gedcom.families[mother.parentFamilyIdentity]
                    if motherFamily.husbandIdentity is not None:
                        rows[0].append((motherFamily.husbandIdentity, 2))
                    if motherFamily.wifeIdentity is not None:
                        rows[0].append((motherFamily.wifeIdentity, 0))
                else:
                    rows[1].append((parentFamily.wifeIdentity, 1))
        width = 0
        # Decide the required width.
        for columns in rows:
            requiredWidth = len(columns) * 170 - 10
            if requiredWidth > width:
                width = requiredWidth

        # Draw the people.
        self.html.addLine(f'<svg style="vertical-align: top; border: 1px solid black; width: {width}px; height: 270px; background-color: white;" viewBox="0 0 {width} 270" xmlns="http://www.w3.org/2000/svg" version="1.1">')
        # self.html.addLine(f'<svg style="vertical-align: top; border: 1px solid black; background-color: white;" xmlns="http://www.w3.org/2000/svg" version="1.1">')
        y = 5
        previousJoinPoints = []
        for columns in rows:
            familyJoinPoints = []
            x = 5
            for cell in columns:
                # print(f'individual = {cell[0]}, type = {cell[1]}')
                self.drawIndividual(cell[0], x, y)

                if cell[1] % 10 > 0:
                    # Family.
                    partner = self.application.gedcom.individuals[cell[0]]
                    if partner.isMale():
                        familyJoinPoints.append(x+160)
                        self.html.addLine(f'<line x1="{x+150}" y1="{y+20}" x2="{x+170}" y2="{y+20}" stroke="black" />')
                        self.html.addLine(f'<line x1="{x+150}" y1="{y+25}" x2="{x+170}" y2="{y+25}" stroke="black" />')
                    else:
                        familyJoinPoints.append(x-10)
                        self.html.addLine(f'<line x1="{x}" y1="{y+20}" x2="{x-20}" y2="{y+20}" stroke="black" />')
                        self.html.addLine(f'<line x1="{x}" y1="{y+25}" x2="{x-20}" y2="{y+25}" stroke="black" />')

                if cell[1] // 10 > 0:
                    # Child of family one above.
                    joinPoint = (cell[1] // 10) - 1
                    joinHeight = y - 10
                    if joinPoint == 1:
                        joinHeight = y - 15
                    # print(f'joinPoint = {joinPoint}, joinHeight = {joinHeight}')
                    self.html.addLine(f'<line x1="{x+75}" y1="{y}" x2="{x+75}" y2="{joinHeight}" stroke="black" />')

                    if len(previousJoinPoints) > joinPoint:
                        self.html.addLine(f'<line x1="{x+75}" y1="{joinHeight}" x2="{previousJoinPoints[joinPoint]}" y2="{joinHeight}" stroke="black" />')
                        self.html.addLine(f'<line x1="{previousJoinPoints[joinPoint]}" y1="{joinHeight}" x2="{previousJoinPoints[joinPoint]}" y2="{y-45}" stroke="black" />')
                x += 170
            y += 70
            previousJoinPoints = familyJoinPoints
            # print(f'previousJoinPoints = {previousJoinPoints}')

        self.html.addLine('</svg>')



    def showIndividual(self, parameters):
        ''' Show an individual. '''
        identity = parameters['person'] if 'person' in parameters else None
        identity = parameters['id'] if 'id' in parameters else identity

        individual = self.application.gedcom.individuals[identity]
        localSources = []

        parentFamily = None
        if individual.parentFamilyIdentity is not None:
            parentFamily = self.application.gedcom.families[individual.parentFamilyIdentity]

        self.html.clear()
        self.displayToolbar(True, f'edit_individual?id={identity}', None, None, False, False, False, '', self.host)
        self.html.addLine(f"<h1>{individual.getName()}</h1>")

        # Draw a small family tree for the individual.
        self.drawIndividualTree(identity)

        # Person Description.
        self.html.addLine('<p>')

        if individual.media is not None:
            media = self.application.gedcom.media[individual.media[0]]
            self.html.add(f'<a href="app:media?id={media.identity}">')
            self.html.add(f'<img src="file://{self.application.gedcom.mediaFolder}{media.file}" align="right" height="120" />')
            self.html.addLine('</a>')

        # Born details.
        self.html.add(f'<a href="app:individual?person={individual.identity}">{individual.getName()}</a>')
        if len(individual.nameSources) > 0:
            for source in individual.nameSources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        self.html.add(f' was born {individual.birth.date.toLongString()}')
        if len(individual.birth.date.sources) > 0:
            for source in individual.birth.date.sources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        if individual.birth.place is not None:
            self.html.add(f' at {individual.birth.place.toLongString()}')
            if len(individual.birth.place.sources) > 0:
                for source in individual.birth.place.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        self.html.addLine('. ')

        # Family details.
        for familyIdentity in individual.familyIdentities:
            partner = None
            family = self.application.gedcom.families[familyIdentity.identity]
            if family.wifeIdentity is not None:
                if family.wifeIdentity != identity:
                    partner = self.application.gedcom.individuals[family.wifeIdentity]
            if family.husbandIdentity is not None:
                if family.husbandIdentity != identity:
                    partner = self.application.gedcom.individuals[family.husbandIdentity]
            if partner is not None:
                if family.marriage is None:
                    self.html.add(f'{firstCap(individual.heShe())} had a <a href="app:family?id={family.identity}">relationship</a> with ')
                else:
                    if family.marriage.date is not None:
                        self.html.add(f'{firstCap(family.marriage.date.toLongString())}')
                        for source in family.marriage.date.sources:
                            self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                        if individual.birth.date is not None:
                            self.html.add(f' aged {individual.getAge(family.marriage.date)}, ')
                        self.html.add(f' {individual.heShe()}')
                    else:
                        self.html.add(f'{firstCap(individual.heShe())}')
                    self.html.add(f' <a href="app:family?id={family.identity}">')
                    self.html.add('married')
                    for source in family.marriage.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                self.html.add(f'</a> <a href="app:individual?id={partner.identity}">{partner.getName()}</a>')
                if familyIdentity.sources is not None:
                    for source in familyIdentity.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                if family.marriage is not None:
                    if family.marriage.place is not None:
                        self.html.add(f' at {family.marriage.place.toLongString()}')
                        for source in family.marriage.place.sources:
                            self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                self.html.addLine('. ')

            if len(family.childrenIdentities) == 0:
                # self.html.addLine(f'They had no children.')
                pass
            else:
                if len(family.childrenIdentities) == 1:
                    self.html.add(f'They had 1 child')
                else:
                    self.html.add(f'They had {len(family.childrenIdentities)} children')
                for childIdentity in family.childrenIdentities:
                    child = self.application.gedcom.individuals[childIdentity]
                    self.html.add(f', <a href="app:individual?person={child.identity}">{child.getName()}</a>')
                self.html.addLine('. ')

            if family.divorce is not None:
                if family.divorce.date is not None:
                    self.html.add(f'{firstCap(family.divorce.date.toLongString())}')
                    for source in family.divorce.date.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                    self.html.add(' they ')
                else:
                    self.html.add('They ')
                if family.marriage is None:
                    self.html.add('separated')
                else:
                    self.html.add('got divorced')
                for source in family.divorce.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                self.html.addLine('. ')

        # Census.
        if individual.census is not None:
            if True:
                # Census as table.
                self.html.addLine('</p>')
                self.html.addLine('<table class="reference" style="background-color: white; border: 1px solid black;" align="center">')
                for census in individual.census:
                    self.html.add('<tr><td style="text-align: center; white-space: nowrap;">')
                    if census.date is not None:
                        self.html.add(f'{census.date.toLongString()[3:]}</td><td style="text-align: center;">')
                        if individual.birth.date is not None:
                            self.html.add(f'{individual.getYears(census.date)}')
                    else:
                        self.html.add('</td><td>')
                    self.html.add('</td><td>')
                    if census.place is not None:
                        self.html.add(f'{census.place.toLongString()}')
                    self.html.add('</td><td>')
                    if census.tags is not None:
                        for tag in census.tags:
                            if tag.type == 'OCCU':
                                self.html.add(f'{tag.information}')
                    self.html.add('</td><td>')
                    if census.tags is not None:
                        for tag in census.tags:
                            if tag.type == 'NOTE':
                                if tag.information.startswith('Living with'):
                                    self.html.add(f' {tag.information[11:]}')
                                    if tag.tags is not None:
                                        for childTag in tag.tags:
                                            self.html.add(f', {childTag.information}')
                    self.html.add('</td><td style="text-align: right;">')
                    for source in census.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                    self.html.addLine('</td></tr>')
                self.html.addLine('</table>')

                self.html.add('<p>')
            else:
                # Census as continue description.
                for census in individual.census:
                    if census.date is not None:
                        self.html.add(f'{firstCap(census.date.toLongString())}')
                        if individual.birthDate is not None:
                            self.html.add(f' aged {individual.getAge(census.date)}, ')
                    self.html.add(f'{individual.heShe()} was living at ')
                    if census.place is not None:
                        self.html.add(f'{census.place.toLongString()}')
                    for source in census.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                    if census.tags is not None:
                        for tag in census.tags:
                            if tag.type == 'OCCU':
                                self.html.add(f' working as a {tag.information}')
                            if tag.type == 'NOTE':
                                if tag.information.startswith('Living with'):
                                    self.html.add(f' living with {tag.information[11:]}')
                    self.html.addLine('. ')

        # Facts.
        if individual.tags is not None:
            for tag in individual.tags:
                if tag.type == 'OCCU':
                    self.html.add(f'{firstCap(individual.heShe())} worked as a')
                    if tag.information[0:1] in 'AEIOU':
                        self.html.add('n')
                    self.html.add(f' {tag.information}')
                elif tag.type == 'EDUC':
                    self.html.add(f'{firstCap(individual.heShe())} was educated at {tag.information}')
                elif tag.type == 'NOTE':
                    if tag.information[0:1] >= 'A' and tag.information[0:1] <= 'Z':
                        self.html.add(tag.toLongString())
                    else:
                        self.html.add(f'{firstCap(individual.heShe())} {tag.toLongString()}')
                else:
                    # Unknown tag type.
                    self.html.add(f'{tag.type} {tag.information}')
                for source in tag.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                if self.html._contents[-1:] == '.':
                    self.html.addLine(' ')
                else:
                    self.html.addLine('. ')

        # Death details.
        if individual.death is not None:
            if individual.death.date is not None:
                self.html.add(f'{firstCap(individual.heShe())} died {individual.death.date.toLongString()}</a>')
                for source in individual.death.date.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                if individual.birth.date is not None:
                    self.html.add(f' when {individual.heShe()} was {individual.getAge(individual.death.date)} old')
            if individual.death.place is not None:
                self.html.add(f' at {individual.death.place.toLongString()}')
                for source in individual.death.place.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
            self.html.addLine('. ')

        # Parents details.
        if parentFamily is not None:
            father = None
            if parentFamily.husbandIdentity is not None:
                father = self.application.gedcom.individuals[parentFamily.husbandIdentity]
                self.html.add(f'{firstCap(individual.hisHer())} father was <a href="app:individual?person={father.identity}">{father.getName()}</a>')
                if father.death is not None and father.death.date is not None:
                    self.html.add(f' who died {father.death.date.toLongString()} when {individual.firstName} was {individual.getAge(father.death.date)} old')
                self.html.addLine('.')
            mother = None
            if parentFamily.wifeIdentity is not None:
                mother = self.application.gedcom.individuals[parentFamily.wifeIdentity]
                self.html.add(f'{firstCap(individual.hisHer())} mother was <a href="app:individual?person={mother.identity}">{mother.getName()}</a>')
                if mother.death is not None and mother.death.date is not None:
                    self.html.add(f' who died {mother.death.date.toLongString()} when {individual.firstName} was {individual.getAge(mother.death.date)} old')
                self.html.addLine('.')

            #if father is not None and mother is not None:
            #    self.html.addLine(f'{firstCap(individual.hisHer())} parents were <a href="app:individual?person={father.identity}">{father.getName()}</a> and <a href="app:individual?person={mother.identity}">{mother.getName()}</a>.')

        self.html.addLine('</p>')

        # Add the sources that have not been used.
        for source in individual.sources:
            self.addLocalSource(localSources, source)

        # Display the sources referenced in this document.
        self.displayLocalSources(localSources)

        # Show the todo for this individual.
        if individual.todos is not None:
            self.html.addLine('<p><a href="app:todo">To Do</a></p>')
            self.html.addLine('<table>')
            for todo in individual.todos:
                self.html.add('<tr>')
                self.html.add(f'<td style="border: 1px solid black; background-color: white; padding: 2px;">{todo.rank}</td>')
                self.html.add(f'<td style="border: 1px solid black; background-color: white; padding: 2px;">{todo.description}</td>')
                self.html.addLine('<tr>')
            self.html.addLine('</table>')

        # Media
        if individual.media is not None:
            if len(individual.media) > 1:
                self.html.addLine('<div style="padding: 5px;">')
                isFirst = True
                for identity in individual.media:
                    if isFirst:
                        isFirst = False
                    else:
                        media = self.application.gedcom.media[identity]
                        self.html.add(f'<a href="app:media?id={media.identity}">')
                        self.html.add(media.toImage(120))
                        self.html.addLine('</a>')
                self.html.addLine('</div>')

        # Show the last change.
        if individual.change is not None:
            self.html.addLine(f'<p class="change">Last change {individual.change.toLongString()}</p>')

        # Show the gedcom data for this individual.
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in individual.gedcomFile:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')
        gedcom = individual.toGedCom()
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in gedcom:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')



    def showFamily(self, parameters):
        ''' Show a family. '''
        identity = parameters['id'] if 'id' in parameters else identity
        family = self.application.gedcom.families[identity]
        localSources = []

        self.html.clear()
        self.displayToolbar(True, f'edit_family?id={identity}', None, None, False, False, False, '', self.host)
        # self.html.addLine(f"<h1>{family.identity} {family.getName()}</h1>")
        self.html.addLine(f"<h1>{family.getName()}</h1>")

        # Draw a small family tree for the family.
        self.drawFamilyTree(identity)

        # Show a description of this family.
        self.html.add('<p>')
        if family.marriage is None:
            pass
            # self.html.add(f'{firstCap(individual.heShe())} had a <a href="app:family?id={family.identity}">relationship</a> with ')
        else:
            if family.marriage.date is not None:
                self.html.add(f'{firstCap(family.marriage.date.toLongString())}')
                for source in family.marriage.date.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                self.html.add(' ')
        husband = None
        wife = None
        if family.husbandIdentity is not None:
            husband = self.application.gedcom.individuals[family.husbandIdentity]
            self.html.add(f'<a href="app:individual?id={family.husbandIdentity}">{husband.getName()}</a>')
            if family.marriage is not None and family.marriage.date is not None:
                self.html.add(f'<span class="age">({husband.getYears(family.marriage.date)})</span>')
        if family.wifeIdentity is not None:
            wife = self.application.gedcom.individuals[family.wifeIdentity]
            self.html.add(' and ')
            self.html.add(f'<a href="app:individual?id={family.wifeIdentity}">{wife.getName()}</a>')
            if family.marriage is not None and family.marriage.date is not None:
                self.html.add(f'<span class="age">({wife.getYears(family.marriage.date)})</span>')
        if family.marriage is None:
            self.html.add(' had a relationship')
        else:
            self.html.add(' got married')
            for source in family.marriage.sources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
            if family.marriage.place is not None:
                self.html.add(f' at {family.marriage.place.toLongString()}')
                for source in family.marriage.place.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        self.html.add('. ')

        if len(family.childrenIdentities) == 0:
            # self.html.addLine(f'They had no children.')
            pass
        else:
            if len(family.childrenIdentities) == 1:
                self.html.add(f'They had 1 child')
            else:
                self.html.add(f'They had {len(family.childrenIdentities)} children')
            for childIdentity in family.childrenIdentities:
                child = self.application.gedcom.individuals[childIdentity]
                self.html.add(f', <a href="app:individual?person={child.identity}">{child.getName()}</a>')
            self.html.addLine('. ')

        if family.divorce is not None:
            if family.divorce.date is not None:
                self.html.add(f'{firstCap(family.divorce.date.toLongString())}')
                for source in family.divorce.date.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                self.html.add(' they ')
            else:
                self.html.add('They ')
            if family.marriage is None:
                self.html.add('separated')
            else:
                self.html.add('got divorced')
            for source in family.divorce.sources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
            self.html.addLine('. ')

        self.html.addLine('</p>')

        # Display the sources referenced in this document.
        self.displayLocalSources(localSources)

        # Show the last change.
        if family.change is not None:
            self.html.addLine(f'<p class="change">Last change {family.change.toLongString()}</p>')

        # Show the gedcom data for this family.
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in family.gedcomFile:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')
        gedcom = family.toGedCom()
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in gedcom:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')



    def showSource(self, parameters):
        ''' Show an individual. '''
        identity = parameters['id'] if 'id' in parameters else None

        source = self.application.gedcom.sources[identity]

        self.html.clear()
        self.displayToolbar(True, f'edit_source?id={identity}', None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>{source.title}</h1>')

        isUseStandardRender = True

        if source.title.startswith('Marriage'):
            # Marriage certificate.
            grid = None
            if source.tags is not None:
                for tag in source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information
            if grid is not None:
                try:
                    self.html.addLine('<table class="certificate" style="background-color: #ccff99; border: 1px solid black;" align="center" cellpadding="5" cellspacing="5">')
                    self.html.add('<tr><td colspan="7">')
                    if source.date is not None:
                        self.html.add(source.date.theDate.strftime("%Y"))
                    self.html.add(' <span class="marriage">Marriage solemnized at</span> ')
                    if source.place is not None:
                        self.html.add(source.place.toLongString())
                    self.html.addLine('</td></tr>')
                    self.html.add('<tr>')
                    self.html.add('<td><span class=\"marriage\">When Married</span></td>')
                    self.html.add('<td><span class=\"marriage\">Name</span></td>')
                    self.html.add('<td><span class=\"marriage\">Age</span></td>')
                    self.html.add('<td><span class=\"marriage\">Rank or Profession</span></td>')
                    self.html.add('<td><span class=\"marriage\">Residence at the time of marriage</span></td>')
                    self.html.add('<td><span class=\"marriage\">Father\'s Name</span></td>')
                    self.html.add('<td><span class=\"marriage\">Rank of Profession of Father</span></td>')
                    self.html.addLine('</tr>')
                    self.html.add("<tr>")
                    self.html.add('<td rowspan=2 style="white-space: nowrap;">')
                    if source.date is not None:
                        self.html.add(source.date.theDate.strftime("%-d %b %Y"))
                    # when.ToString("d MMM yyyy")
                    self.html.add('</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[1][1]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[1][3]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[1][4]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[1][5]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[3][1]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[3][3]}</td>')
                    self.html.addLine('</tr>')
                    self.html.add('<tr>')
                    #// sbHtml.Append("<td><span class=\"Small\">Bride</span></td>")
                    self.html.add(f'<td style="white-space: nowrap;">{grid[2][1]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[2][3]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[2][4]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[2][5]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[4][1]}</td>')
                    self.html.add(f'<td style="white-space: nowrap;">{grid[4][3]}</td>')
                    self.html.addLine('</tr>')
                    self.html.addLine(f'<tr><td colspan="7"><span class="marriage">in the Presence of us,</span> {grid[5][1]}</td></tr>')
                    self.html.add('<tr><td colspan=7 align=center><span class="marriage">GRO Reference</span> ')
                    self.html.add(grid[0][2])
                    self.html.addLine('</td></tr>')
                    self.html.addLine('</table>')
                    isUseStandardRender = False
                except:
                    self.html.addLine('<h1>Error</h1>')
                    self.html.addLine('<table>')
                    for rows in grid:
                        self.html.add('<tr>')
                        for cell in rows:
                            self.html.add(f'<td style="white-space: nowrap;">\'{cell}\'</td>')
                        self.html.addLine('</tr>')
                    self.html.addLine('</table>')

        elif source.title.startswith('Birth'):
            # Birth Certificate.
            grid = None
            if source.tags is not None:
                for tag in source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information
            if grid is not None:
                try:
                    self.html.addLine('<table class="certificate" style="background-color: mistyrose; border: 1px solid black;" align="center" cellpadding="5" cellspacing="0">')
                    self.html.add('<tr><td colspan="8">')
                    if source.date is not None:
                        self.html.add(source.date.theDate.strftime("%Y"))
                    self.html.addLine(f' <span class="birth">Birth in the registration district of</span> {grid[1][1]}</td></tr>')
                    self.html.add('<tr valign="bottom"><td><span class="birth">When and<br/>Where Born</span></td>')
                    self.html.add('<td class="birth">Name</td>')
                    self.html.add('<td><span class="birth">Sex</span></td>')
                    self.html.add('<td><span class="birth">Father</span></td>')
                    self.html.add('<td><span class="birth">Mother</span></td>')
                    self.html.add('<td><span class="birth">Occupation<br />of Father</span></td>')
                    self.html.add('<td><span class="birth">Informant</span></td>')
                    self.html.addLine('<td><span class="birth">When Registered</span></td></tr>')

                    self.html.add('<tr valign=top><td>')
                    if source.date is not None:
                        # self.html.add(source.date.theDate.strftime("%-d %b %Y"))
                        self.html.add(grid[2][1])
                    self.html.add(f'<br />{grid[2][2]}</td>')
                    self.html.add(f'<td>{grid[3][1]}</td>')
                    self.html.add(f'<td>{grid[3][2]}</td>')
                    self.html.add(f'<td>{grid[5][1]}</td>')
                    self.html.add(f'<td>{grid[4][1]}<br />{grid[4][2]}</td>')
                    self.html.add(f'<td>{grid[5][2]}</td>')
                    self.html.add(f'<td>{grid[6][1]}<br />{grid[6][2]}</td>')
                    self.html.add(f'<td>{grid[7][1]}</td></tr>')
                    self.html.add(f'<tr><td colspan="8" align="center"><span class="birth">GRO Reference</span> {grid[0][2]}</td></tr>')
                    self.html.add('</table>');
                    isUseStandardRender = False
                except:
                    self.html.addLine('<h1>Error</h1>')
                    self.html.addLine('<table>')
                    for rows in grid:
                        self.html.add('<tr>')
                        for cell in rows:
                            self.html.add(f'<td style="white-space: nowrap;">\'{cell}\'</td>')
                        self.html.addLine('</tr>')
                    self.html.addLine('</table>')

        elif source.title.startswith('Death'):
            # Death Cerificate.
            grid = None
            if source.tags is not None:
                for tag in source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information
            if grid is not None:
                try:
                    self.html.addLine('<table class="certificate" style="background-color: thistle; border: 1px solid black;" align=center cellpadding=5 cellspacing=0>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Registration District</span></td><td colspan=3>{grid[1][1]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">When and Where</span></td><td colspan=3>{grid[2][1]}<br/>{grid[3][1]}</td></tr>')
                    self.html.add(f'<tr><td style="text-align: right;"><span class="death">Name</span></td><td>{grid[4][1]}</td>')
                    self.html.addLine(f'<td style="text-align: right;"><span class="death">Sex</span></td><td>{grid[4][2]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Date Place of Birth</span></td><td colspan=3>{grid[5][1]}<br/>{grid[5][2]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Occupation</span></td><td colspan=3>{grid[6][1]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Usual Address</span></td><td colspan=3>{grid[7][1]}</td></tr>')

                    # Cause of death can be multiline.
                    cause = grid[8][1]
                    cause = cause.replace('\n', '<br />')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Cause of Death</span></td><td colspan=3>{cause}</td></tr>')
                    self.html.add(f'<tr><td style="text-align: right;"><span class="death">Informant</span></td><td>{grid[9][1]}</td>')
                    self.html.addLine(f'<td style="text-align: right;"><span class="death">Informant Description</span></td><td>{grid[9][2]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Informant Address</span></td><td colspan=3>{grid[10][1]}</td></tr>')
                    self.html.add(f'<tr><td style="text-align: right;"><span class="death">When Registered</span></td><td>{grid[11][1]}</td>')
                    self.html.addLine(f'<td style="text-align: right;"><span class="death">Reference</span></td><td>{grid[0][2]}</td></tr>')
                    self.html.addLine('</table>')
                    isUseStandardRender = False
                except:
                    self.html.addLine('<h1>Error</h1>')
                    self.html.addLine('<table>')
                    for rows in grid:
                        self.html.add('<tr>')
                        for cell in rows:
                            self.html.add(f'<td style="white-space: nowrap;">\'{cell}\'</td>')
                        self.html.addLine('</tr>')
                    self.html.addLine('</table>')

        elif source.title.startswith('Census') or source.title.startswith('1939 Register'):
            # Census.
            grid = None
            if source.tags is not None:
                for tag in source.tags:
                    if isinstance(tag.information, list):
                        grid = tag.information
            if grid is not None:
                self.html.addLine('<table class="certificate" style="background-color: lightcyan; border: 1px solid black;" align="center" cellpadding="5" cellspacing="0">')
                self.html.add('<tr><td class="census" style="text-align: center;" colspan="5"><span style="font-size: 20pt;">')
                if source.date is not None:
                    self.html.add(source.date.theDate.strftime("%Y"))
                self.html.add(' Census</span> (')
                if source.date is not None:
                    self.html.add(f'{source.date.toLongString()}')
                self.html.add(')</td><tr>')
                self.html.add('<tr><td colspan="5"><table width="100%"><tr>')
                self.html.add('<td align="center"><span class="census">Series</span></td>')
                self.html.add('<td align="center"><span class="census">Piece</span></td>')
                self.html.add('<td align="center"><span class="census">Folio</span></td>')
                self.html.add('<td align="center"><span class="census">Page</span></td>')

                self.html.add('</tr></tr>')

                self.html.add('<td align="center">')
                if len(grid[0]) >= 3:
                    self.html.add(f'{grid[0][3]}')
                self.html.add('</td>')
                self.html.add('<td align="center">')
                if len(grid[0]) >= 5:
                    self.html.add(f'{grid[0][5]}')
                self.html.add('</td>')
                self.html.add('<td align="center">')
                if len(grid[0]) >= 7:
                    self.html.add(f'{grid[0][7]}')
                self.html.add('</td>')
                self.html.add('<td align="center">')
                if len(grid[0]) >= 9:
                    self.html.add(f'{grid[0][9]}')
                self.html.add('</td>')
                self.html.add('</tr></table></td></tr>')

                self.html.add('<tr><td colspan="5"><span class="census">Address</span> ')
                if source.place is not None:
                    self.html.add(source.place.toLongString())
                self.html.add('</td></tr>')
                self.html.add('<tr valign="bottom">');
                self.html.add('<td><span class="census">Name</span></td>')
                #if (theYear == 1939)
                #{
                #    self.html.add("<td><span class=\"Census\">DoB</span></td>");
                #    self.html.add("<td><span class=\"Census\">Sex</span></td>");
                #}
                #else
                #{
                self.html.add('<td><span class="census">Relation<br/>To Head</span></td>')
                self.html.add('<td><span class="census">Age</span></td>')
                #}
                self.html.add('<td><span class="census">Occupation</span></td>')
                #if (theYear == 1939)
                #{
                #    self.html.add("<td><span class=\"Census\">Marital Status</span></td>");
                #}
                #else
                #{
                self.html.add('<td><span class="census">Born Location</span></td>')
                #}
                self.html.add('</tr>')

                count = 0
                for rows in grid:
                    if count > 0:
                        self.html.add('<tr>')
                        if rows[1] == '':
                            self.html.add(f'<td>{rows[0]}</td>')
                        else:
                            self.html.add(f'<td><a href="app:individual?id={rows[1]}">{rows[0]}</a></td>')
                        if len(rows) > 2:
                            self.html.add(f'<td>{rows[3]}</td>')
                            self.html.add(f'<td>{rows[2]}</td>')
                            if len(rows) > 4:
                                self.html.add(f'<td>{rows[4]}</td>')
                                self.html.add(f'<td>{rows[5]}</td>')
                        self.html.addLine('</tr>')
                    count += 1
                self.html.addLine('</table>')
                isUseStandardRender = False

        # The default render
        if isUseStandardRender:
            # General source.
            if source.date is not None:
                self.html.addLine(f'<p>{source.date.toLongString()}</p>')
            if source.place is not None:
                self.html.addLine(f'<p>{source.place.toLongString()}</p>')
            if source.tags is not None:
                for tag in source.tags:
                    self.html.addLine(f'<p>{tag.toLongString()}</p>')
        else:
            # Show any extra tags.
            if source.tags is not None:
                for tag in source.tags:
                    if not isinstance(tag.information, list):
                        self.html.addLine(f'<p>{tag.toLongString()}</p>')

        # Show the last change.
        if source.change is not None:
            self.html.addLine(f'<p class="change">Last change {source.change.toLongString()}</p>')

        # Show the people that reference this source.
        self.html.addLine('<p>Individuals</p>')
        self.html.addLine('<table class="reference">')
        for individual in self.application.gedcom.individuals.values():
            tags = ''
            # print(f'{individual.identity} {individual.getName()}')
            if identity in individual.sources:
                tags += ' '
            if identity in individual.nameSources:
                tags += 'Name, '
            if individual.birth is not None:
                if individual.birth.date is not None:
                    if identity in individual.birth.date.sources:
                        tags += 'Birth Date, '
                if individual.birth.place is not None:
                    if identity in individual.birth.place.sources:
                        tags += 'Birth Place, '
                if identity in individual.birth.sources:
                    tags += 'Birth, '
            if individual.death is not None:
                if individual.death.date is not None:
                    if identity in individual.death.date.sources:
                        tags += 'Death Date, '
                if individual.death.place is not None:
                    if identity in individual.death.place.sources:
                        tags += 'Death Place, '
                if identity in individual.death.sources:
                    tags += 'Death, '
            if individual.census is not None:
                for census in individual.census:
                    if census.sources is not None:
                        if identity in census.sources:
                            tags += f'Census {census.date.theDate.year}, '
            if tags != '':
                self.html.addLine(f'<tr><td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td><td>{tags[:-2]}</td></tr>')
        self.html.addLine('</table>')

        # Show the families that reference this source.
        self.html.addLine('<p>Families</p>')
        self.html.addLine('<table class="reference">')
        for family in self.application.gedcom.families.values():
            tags = ''
            if family.marriage is not None:
                if family.marriage.date is not None:
                    if identity in family.marriage.date.sources:
                        tags += 'Marriage Date, '
                if family.marriage.place is not None:
                    if identity in family.marriage.place.sources:
                        tags += 'Marriage Place, '
            if family.divorce is not None:
                if identity in family.divorce.sources:
                    tags += 'Divorce, '
                if family.divorce.date is not None:
                    if identity in family.divorce.date.sources:
                        tags += 'Divorce Date, '

            if tags != '':
                self.html.addLine(f'<tr><td><a href="app:family?id={family.identity}">{family.getName()}</a></td><td>{tags[:-2]}</td></tr>')
        self.html.addLine('</table>')

        # Show the gedcom data for this source.
        # The div is only needed to see both loaded and calculated gedcom.
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in source.gedcomFile:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')
        gedcom = source.toGedCom()
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in gedcom:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')



    def showMedia(self, parameters):
        ''' Show a media object. '''
        identity = parameters['id'] if 'id' in parameters else None

        media = self.application.gedcom.media[identity]

        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>{media.title}</h1>')
        self.html.addLine(f'<div><img src="file://{self.application.gedcom.mediaFolder}{media.file}" /></div>')

        # Show the people that reference this source.
        self.html.addLine('<p>Individuals</p>')
        self.html.addLine('<table class="reference">')
        for individual in self.application.gedcom.individuals.values():
            isShow = False
            if individual.media is not None:
                if identity in individual.media:
                    isShow = True

            if isShow:
                self.html.addLine(f'<tr><td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td></tr>')
        self.html.addLine('</table>')

        # Show the gedcom data for this media.
        # The div is only needed to see both loaded and calculated gedcom.
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in media.gedcomFile:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')
        gedcom = media.toGedCom()
        self.html.add('<div style="display: inline-block; vertical-align:top;">')
        self.html.add('<pre style="border: 1px solid black;  background-color: white;">')
        for line in gedcom:
            indent = int(line[:1])
            self.html.addLine(f'{"  " * indent}{html.escape(line)}')
        self.html.addLine('</pre></div>')



    def showToDo(self, parameters):
        ''' Show all the ToDos. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>All To Do\'s</h1>')
        todos = []
        for individual in self.application.gedcom.individuals.values():
            if individual.todos is not None:
                for todo in individual.todos:
                    todos.append(todo)

        # Sort the todos.
        todos.sort(key=toDoRank)

        # Display the todos.
        self.html.addLine('<table>')
        for todo in todos:
            self.html.add('<tr>')
            self.html.add(f'<td style="border: 1px solid black; background-color: white; padding: 3px;"><a href="app:individual?id={todo.individual.identity}">{todo.individual.getName()}</a></td>')
            self.html.add(f'<td style="border: 1px solid black; background-color: white; padding: 3px; text-align: right;">{todo.rank}</td>')
            self.html.add(f'<td style="border: 1px solid black; background-color: white; padding: 3px;">{todo.description}</td>')
            self.html.addLine('<tr>')
        self.html.addLine('</table>')



    def showAll(self, parameters):
        ''' Show all elements. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>All Elements</h1>')
        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Individuals</legend>')
        self.html.addLine(f'<table>')
        for individual in self.application.gedcom.individuals.values():
            self.html.add('<tr>')
            self.html.add(f'<td>{individual.identity}</td>')
            self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
            self.html.addLine('</tr>')
        self.html.add('</table>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Families</legend>')
        self.html.addLine(f'<table>')
        for family in self.application.gedcom.families.values():
            self.html.add('<tr>')
            self.html.add(f'<td>{family.identity}</td>')
            self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
            self.html.addLine('</tr>')
        self.html.add('</table>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Sources</legend>')
        self.html.addLine(f'<table>')
        for source in self.application.gedcom.sources.values():
            self.html.add('<tr>')
            self.html.add(f'<td>{source.identity}</td>')
            self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
            self.html.addLine('</tr>')
        self.html.add('</table>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Media</legend>')
        self.html.addLine(f'<table>')
        for media in self.application.gedcom.media.values():
            self.html.add('<tr>')
            self.html.add(f'<td>{media.identity}</td>')
            self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
            self.html.addLine('</tr>')
        self.html.add('</table>')
        self.html.addLine('</fieldset>')



    def displayAllPlacesWithParent(self, parent):
        ''' Show all places with the specified parent. '''
        childPlaces = []
        if parent is None:
            for place in Place.allPlaces.values():
                if place.parent is None:
                    childPlaces.append(place)
        else:
            for place in Place.allPlaces.values():
                if place.parent == parent:
                    childPlaces.append(place)
        childPlaces.sort(key=Place.byName)
        self.html.addLine('<p>Child Locations</p>')
        self.html.addLine('<table style="display: inline-block; vertical-align:top; border: 1px solid black;">')
        for place in childPlaces:
            if place.placeType != PlaceType.ADDRESS:
                self.html.add(f'<tr style="border-bottom: 1px solid black;"><td><a href="app:place?id={place.identity}">{place.name}</a></td>')
                if place.placeType == PlaceType.COUNTRY:
                    self.html.add('<td>Country</td>')
                else:
                    self.html.add('<td>Place</td>')
                if place.latitude is not None:
                    self.html.add(f'<td style="text-align: center;">{place.latitude}</td>')
                else:
                    self.html.add('<td></td>')
                if place.longitude is not None:
                    self.html.add(f'<td style="text-align: center;">{place.longitude}</td>')
                else:
                    self.html.add('<td></td>')
                self.html.addLine('</tr>')
        self.html.addLine('</table>')

        self.html.addLine('<table style="display: inline-block; vertical-align:top; border: 1px solid black;">')
        for place in childPlaces:
            if place.placeType == PlaceType.ADDRESS:
                self.html.add(f'<tr style="border-bottom: 1px solid black;"><td><a href="app:place?id={place.identity}">{place.name}</a></td>')
                self.html.add('<td>Address</td>')
                if place.latitude is not None:
                    self.html.add(f'<td style="text-align: center;">{place.latitude}</td>')
                else:
                    self.html.add('<td></td>')
                if place.longitude is not None:
                    self.html.add(f'<td style="text-align: center;">{place.longitude}</td>')
                else:
                    self.html.add('<td></td>')
                self.html.addLine('</tr>')
        self.html.addLine('</table>')




    def showAllPlaces(self, parameters):
        ''' Show all places. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>All Elements</h1>')

        self.displayAllPlacesWithParent(None)



    def showPlace(self, parameters):
        ''' Show a single place. '''
        placeName = parameters['id'] if 'id' in parameters else None
        placeName = placeName.replace('%20', ' ')

        place = Place.allPlaces[placeName]

        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>{place.name}</h1>')
        if place.parent is not None:
            self.html.addLine(f'<p>Parent: \'{place.parent.toLongString()}\'</p>')
        if place.placeType == PlaceType.ADDRESS:
            self.html.addLine(f'<p>Type: Address</p>')
        elif place.placeType == PlaceType.COUNTRY:
            self.html.addLine(f'<p>Type: Country</p>')
        else:
            self.html.addLine(f'<p>Type: Place</p>')
        if place.latitude is not None:
            self.html.addLine(f'<p>Latitude: {place.latitude}</p>')
        if place.longitude is not None:
            self.html.addLine(f'<p>Longitude: {place.longitude}</p>')

        # Display a map.
        if place.latitude is not None and place.longitude is not None:
            #
            # <iframe> does not work.  So this is not going to work.
            #

            # self.html.add('<iframe width="800" height="450" frameborder="1" style="border: 1px solid black;" ')
            ##### self.html.add(f'src="https://www.openstreetmap.org/#map=10/{place.latitude}/{place.longitude}" ')
            ##### self.html.add(f'src="https://www.openstreetmap.org/export/embed.html?#map=10/{place.latitude}/{place.longitude}" ')
            # self.html.add('allowfullscreen>')
            # self.html.addLine('</iframe>')
            pass

        self.displayAllPlacesWithParent(place)

        # Show the people that reference this place.
        self.html.addLine('<p>Individuals</p>')
        self.html.addLine('<table class="reference">')
        for individual in self.application.gedcom.individuals.values():
            tags = ''
            # print(f'{individual.identity} {individual.getName()}')

            if individual.birth is not None:
                if individual.birth.place is not None:
                    if place.identity in individual.birth.place.toIdentityCheck():
                        tags += 'Birth Place, '
            if individual.death is not None:
                if individual.death.place is not None:
                    if place.identity in individual.death.place.toIdentityCheck():
                        tags += 'Death Place, '
            if individual.census is not None:
                for census in individual.census:
                    if census.place is not None:
                        if place.identity in census.place.toIdentityCheck():
                            tags += f'Census {census.date.theDate.year}, '
            if individual.tags is not None:
                for tag in individual.tags:
                    if tag.place is not None:
                        if place.identity in tag.place.toIdentityCheck():
                            tags += ', '
            if tags != '':
                self.html.addLine(f'<tr><td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td><td>{tags[:-2]}</td></tr>')
        self.html.addLine('</table>')

        # Show the families that reference this place.
        self.html.addLine('<p>Families</p>')
        self.html.addLine('<table class="reference">')
        for family in self.application.gedcom.families.values():
            tags = ''
            if family.marriage is not None:
                if family.marriage.place is not None:
                    if place.identity in family.marriage.place.toIdentityCheck():
                        tags += 'Marriage Place, '
            if tags != '':
                self.html.addLine(f'<tr><td><a href="app:family?id={family.identity}">{family.getName()}</a></td><td>{tags[:-2]}</td></tr>')
        self.html.addLine('</table>')

        # Show the sources that reference this place.
        self.html.addLine('<p>Source</p>')
        self.html.addLine('<table class="reference">')
        for source in self.application.gedcom.sources.values():
            tags = ''
            if source.place is not None:
                if place.identity in source.place.toIdentityCheck():
                    tags += ', '
            if tags != '':
                self.html.addLine(f'<tr><td><a href="app:source?id={source.identity}">{source.title}</a></td><td>{tags[:-2]}</td></tr>')
        self.html.addLine('</table>')
