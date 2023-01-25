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
        }



    def showAbout(self, _paramtersDictionary):
        ''' Render the about page on the :py:class:`Html` object. '''
        # Clear the html object.
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False)

        self.html.addLine("<h1>About Formula One Results Database</h1>")
        self.html.addLine("<p>by Steven Walton &copy; 1985-2022</p>")

        self.html.addLine("<hr/>")
        self.html.addLine("<table>")
        self.html.addLine("<tr><td>Linux</td><td>Python</td><td>2011-2022</td></tr>")
        self.html.addLine("<tr><td>Windows&trade;</td><td>Access</td><td>1995-2011</td></tr>")
        self.html.addLine("<tr><td>Amiga</td><td>GFA Basic</td><td>1990-1995</td></tr>")
        self.html.addLine("<tr><td>BBC Model B</td><td>BBC Basic</td><td>1985-1990</td></tr>")
        self.html.addLine("</table>")

        self.html.addLine('<hr/>')
        self.html.addLine('<table>')
        self.html.addLine('<tr class="title"><td>Pos</td><td>Driver</td><td>Team</td><td>Results</td><td>Points</td></tr>')
        self.html.addLine('<tr><td class="rank" style="text-align: right;">1</td><td class="driver">Ayrton Senna</td><td class="team">McLaren Honda</td><td class="resultslist">12.1</td><td class="pts">43</td></tr>')
        self.html.addLine('<tr><td class="rank" style="text-align: right;">2</td><td class="driver">Nigel Mansell</td><td class="team">Williams Renault</td><td class="resultslist">.1.2</td><td class="pts">21</td></tr>')
        self.html.addLine('<tr><td class="rank" style="text-align: right;">rank</td><td class="driver">driver</td><td class="team">team</td><td class="resultslist">resultslist</td><td class="racewins">racewins</td><td class="racepodium">racepodium</td><td class="racetop6">racetop6</td><td class="racetop10">racetop10</td><td class="racetop20">racetop20</td><td class="poles">poles</td><td class="laps">laps</td><td class="retired">retired</td><td class="pts">pts</td><td class="difference">difference</td><td class="races">races</td></tr>')
        self.html.addLine('</table>')
        self.html.addLine('<hr/>')

        self.html.addLine('<div style="white-space: nowrap; display: table; margin: 0 auto;">')
        self.html.addLine('<div style="display: inline-block; vertical-align: top;">')
        self.html.addLine('<fieldset style="display: inline-block;"><legend>Fieldset 1</legend>')
        self.html.addLine('<table>')
        self.html.addLine('<tr class="title"><td>Pos</td><td>Driver</td><td>Results</td></tr>')
        self.html.addLine('<tr class="winner"><td style="text-align: right;">1</td><td class="driver">Ayrton Senna <span class="years">(1984-1994)</span></td><td class="pts">43</td></tr>')
        self.html.addLine('<tr><td style="text-align: right;">2</td><td class="driver">Nigel Mansell <span class="years">(1981-1994)</span></td><td class="pts">21</td></tr>')
        self.html.addLine('<tr><td style="text-align: right;">3</td><td class="driver">Lella Lombardi &#x2640; <span class="years">(1981-1994)</span></td><td class="pts">21</td></tr>')

        self.html.addLine('<tr><td style="text-align: right;">10</td><td class="driver">class="driver"</td><span class="years">class="years"</span><td class="pts">class="pts"</td></tr>')
        self.html.addLine('</table>')
        self.html.addLine('</fieldset>')

        self.html.addLine('<br />')
        self.html.addLine('<fieldset style="display: inline-block;"><legend>Fieldset 2</legend>')
        self.html.addLine('<table>')
        self.html.addLine('<tr><td class="date">12-Nov-2011</td><td>2nd</td><td>German</td></tr>')
        self.html.addLine('<tr><td class="date">12-Nov-2011</td><td>2nd</td><td>German<br/>Grand Prix</td></tr>')
        self.html.addLine('<tr><td class="date">12-Nov-2011</td><td>2nd</td><td>German</td></tr>')
        self.html.addLine('</table>')
        self.html.addLine('</fieldset>')
        self.html.addLine('</div>')

        self.html.addLine('<div style="display: inline-block; vertical-align: top;">')
        self.html.addLine('<fieldset "style="display: inline-block;"><legend>Fieldset 3</legend>')
        self.html.addLine('<h1>Fonts Testing</h1>')
        self.html.addLine('<p>Hello from Standard unstyled text.</p>')
        self.html.addLine('<p style="font-family: sans-serif;">Hello from sans-serif.</p>')
        self.html.addLine('<p style="font-family: Liberation Sans, sans-serif;">Hello from Liberation Sans, sans-serif.</p>')
        self.html.addLine('<p style="font-family: Verdana, sans-serif;">Hello from Verdana, sans-serif.</p>')
        self.html.addLine('<p style="font-family: Arial, Helvetica, sans-serif;">Hello from Arial, Helvetica, sans-serif.</p>')
        self.html.addLine('<p style="font-family: Tahoma, Geneva, sans-serif;">Hello from Tahoma, Geneva, sans-serif.</p>')
        self.html.addLine('<p style="font-family: DejaVu Sans, sans-serif;">Hello from DejaVu Sans, sans-serif.</p>')
        self.html.addLine('<p style="font-family: FreeSans, sans-serif;">Hello from FreeSans, sans-serif.</p>')

        self.html.addLine('<p style="font-family: serif;">Hello from serif.</p>')
        self.html.addLine('<p style="font-family: Georgia, serif;">Hello from Georgia, serif.</p>')
        self.html.addLine('<p style="font-family: Times New Roman, Times, serif;">Hello from Times New Roman, Times, serif.</p>')

        self.html.addLine('<p style="font-family: Liberation Mono, monospace;">Hello from Liberation Mono, monospace.</p>')
        self.html.addLine('<p style="font-family: FreeMono, monospace;">Hello from FreeMono, monospace.</p>')
        self.html.addLine('<p style="font-family: Source Code Pro, monospace;">Hello from Source Code Pro, monospace.</p>')
        self.html.addLine('</fieldset>')
        self.html.addLine('</div>')
        self.html.addLine('</div>')

        # Menu Test
        self.html.addLine('<hr/>')
        self.html.addLine('<script>')

        self.html.addLine('var timerID = null;')
        self.html.addLine('var timerOn = false;')
        self.html.addLine('var timecount = 1000;')
        self.html.addLine('var what = "moz";')
        self.html.addLine('var newbrowser = true;')
        self.html.addLine('var check = true;')

        self.html.addLine('function showLayer(layerName)')
        self.html.addLine('{')
        self.html.addLine('    if(check)')
        self.html.addLine('    {')
        self.html.addLine('        if (what =="none")')
        self.html.addLine('        {')
        self.html.addLine('            return;')
        self.html.addLine('        }')
        self.html.addLine('        else if (what == "moz")')
        self.html.addLine('        {')
        self.html.addLine('            document.getElementById(layerName).style.visibility="visible";')
        self.html.addLine('        }')
        self.html.addLine('        else')
        self.html.addLine('        {')
#        self.html.addLine('            eval(layerRef+'["'+layerName+'"]'+styleSwitch+'.visibility="visible"');')
        self.html.addLine('        }')
        self.html.addLine('    }')
        self.html.addLine('    else')
        self.html.addLine('    {')
        self.html.addLine('        // alert ("Please wait for the page to finish loading.");')
        self.html.addLine('        return;')
        self.html.addLine('    }')
        self.html.addLine('}')

        self.html.addLine('function hideLayer(layerName)')
        self.html.addLine('{')
        self.html.addLine('    if(check)')
        self.html.addLine('    {')
        self.html.addLine('        if (what =="none")')
        self.html.addLine('        {')
        self.html.addLine('            return;')
        self.html.addLine('        }')
        self.html.addLine('        else if (what == "moz")')
        self.html.addLine('        {')
        self.html.addLine('            document.getElementById(layerName).style.visibility="hidden";')
        self.html.addLine('        }')
        self.html.addLine('        else')
        self.html.addLine('        {')
#        self.html.addLine('            eval(layerRef+'["'+layerName+'"]'+styleSwitch+'.visibility="hidden"');')
        self.html.addLine('        }')
        self.html.addLine('    }')
        self.html.addLine('    else')
        self.html.addLine('    {')
        self.html.addLine('        // alert ("Please wait for the page to finish loading.");')
        self.html.addLine('        return;')
        self.html.addLine('    }')
        self.html.addLine('} ')

        self.html.addLine('function hideAll()')
        self.html.addLine('{')
        self.html.addLine('    hideLayer("menu1");')
#        self.html.addLine('//    hideLayer('layer2');')
#        self.html.addLine('//    hideLayer('layer3');
#        self.html.addLine('//    hideLayer('layer4');
        self.html.addLine('}')

        self.html.addLine('function startTimer()')
        self.html.addLine('{')
        self.html.addLine('    if (timerOn == false)')
        self.html.addLine('    {')
        self.html.addLine('        timerID=setTimeout( "hideAll()" , timecount);')
        self.html.addLine('        timerOn = true;')
        self.html.addLine('    }')
        self.html.addLine('} ')

        self.html.addLine('function stopTimer()')
        self.html.addLine('{')
        self.html.addLine('    if (timerOn)')
        self.html.addLine('    {')
        self.html.addLine('        clearTimeout(timerID);')
        self.html.addLine('        timerID = null;')
        self.html.addLine('        timerOn = false;')
        self.html.addLine('    }')
        self.html.addLine('} ')

        self.html.addLine('</script>')
        self.html.addLine('<h1>Menu Test</h1>')
        self.html.addLine('<p style="background-color: red;" onmouseover="showLayer(\'menu1\'); stopTimer();" onmouseout="startTimer();">Menu</p>')
        self.html.addLine('<div id="menu1" style="visibility: hidden;">Menu 1<br/>Menu 2</div>')

        # Set the page flags.
        self.levels = None



    def showHome(self, parameters):
        ''' Render the home page. '''
        #if self.application.gedcom.defaultIdentity is not None:
        #    self.showIndividual({'person': self.application.gedcom.defaultIdentity})
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine('<h1>Home</h1>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Individuals</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        count = 0
        individuals = []
        for individual in self.application.gedcom.individuals.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td>{individual.identity}</td>')
                self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
                self.html.addLine('</tr>')
                lastChange = individual
            individuals.append(individual)
        self.html.add('<td>Last</td>')
        self.html.add(f'<td>{individual.identity}</td>')
        self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
        self.html.addLine('</tr>')

        # Recent.
        individuals.sort(key=individual.byChange, reverse=True)
        for index in range(10):
            individual = individuals[index]
            self.html.add('<tr>')
            self.html.add(f'<td>Recent {index + 1}</td>')
            self.html.add(f'<td>{individual.identity}</td>')
            self.html.add(f'<td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td>')
            self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are {len(individuals)} individuals in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Families</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        families = []
        for family in self.application.gedcom.families.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td>{family.identity}</td>')
                self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
                self.html.addLine('</tr>')
            families.append(family)
        self.html.add('<tr>')
        self.html.add('<td>Last</td>')
        self.html.add(f'<td>{family.identity}</td>')
        self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
        self.html.addLine('</tr>')

        # Recent.
        families.sort(key=family.byChange, reverse=True)
        for index in range(10):
            family = families[index]
            self.html.add('<tr>')
            self.html.add(f'<td>Recent {index + 1}</td>')
            self.html.add(f'<td>{family.identity}</td>')
            self.html.add(f'<td><a href="app:family?id={family.identity}">{family.getName()}</a></td>')
            self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are {len(families)} families in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Sources</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        sources = []
        for source in self.application.gedcom.sources.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td>{source.identity}</td>')
                self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
                self.html.addLine('</tr>')
                self.html.add('<tr>')
            sources.append(source)
        self.html.add('<td>Last</td>')
        self.html.add(f'<td>{source.identity}</td>')
        self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
        self.html.addLine('</tr>')

        # Recent.
        sources.sort(key=source.byChange, reverse=True)
        for index in range(10):
            source = sources[index]
            self.html.add('<tr>')
            self.html.add(f'<td>Recent {index + 1}</td>')
            self.html.add(f'<td>{source.identity}</td>')
            self.html.add(f'<td><a href="app:source?id={source.identity}">{source.getName()}</a></td>')
            self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are {len(sources)} sources in this gedcom.</p>')
        self.html.addLine('</fieldset>')

        self.html.add('<fieldset style="display: inline-block; vertical-align:top;">')
        self.html.addLine(f'<legend>Media</legend>')
        self.html.addLine(f'<table>')
        isFirst = True
        mediaObjects = []
        for media in self.application.gedcom.media.values():
            if isFirst:
                isFirst = False
                self.html.add('<tr>')
                self.html.add('<td>First</td>')
                self.html.add(f'<td>{media.identity}</td>')
                self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
                self.html.addLine('</tr>')
                self.html.add('<tr>')
            mediaObjects.append(media)
        self.html.add('<td>Last</td>')
        self.html.add(f'<td>{media.identity}</td>')
        self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
        self.html.addLine('</tr>')

        # Recent.
        sources.sort(key=media.byChange, reverse=True)
        for index in range(10):
            media = mediaObjects[index]
            self.html.add('<tr>')
            self.html.add(f'<td>Recent {index + 1}</td>')
            self.html.add(f'<td>{media.identity}</td>')
            self.html.add(f'<td><a href="app:media?id={media.identity}">{media.getName()}</a></td>')
            self.html.addLine('</tr>')

        self.html.add('</table>')
        self.html.addLine(f'<p>There are {len(mediaObjects)} media in this gedcom.</p>')
        self.html.addLine('</fieldset>')




    def showIndex(self, _parameters):
        ''' Render the index page. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)

        self.html.addLine('<h1>Index</h1>')
        self.html.addLine('<ul>')
        self.html.addLine('<li><a href="app:todo">ToDos</a></li>')
        self.html.addLine('<li><a href="app:all">All Elements</a></li>')
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
            if parentFamily.husbandIdentity is not None:
                rows[1].append((parentFamily.husbandIdentity, 11))
                father = self.application.gedcom.individuals[parentFamily.husbandIdentity]
                if father.parentFamilyIdentity is not None:
                    fatherFamily = self.application.gedcom.families[father.parentFamilyIdentity]
                    if fatherFamily.husbandIdentity is not None:
                        rows[0].append((fatherFamily.husbandIdentity, 1))
                    if fatherFamily.wifeIdentity is not None:
                        rows[0].append((fatherFamily.wifeIdentity, 0))
            if parentFamily.wifeIdentity is not None:
                rows[1].append((parentFamily.wifeIdentity, 21))
                mother = self.application.gedcom.individuals[parentFamily.wifeIdentity]
                if mother.parentFamilyIdentity is not None:
                    motherFamily = self.application.gedcom.families[mother.parentFamilyIdentity]
                    if motherFamily.husbandIdentity is not None:
                        rows[0].append((motherFamily.husbandIdentity, 2))
                    if motherFamily.wifeIdentity is not None:
                        rows[0].append((motherFamily.wifeIdentity, 0))
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
                self.html.addLine('<table style="background-color: white; border: 1px solid black;">')
                for census in individual.census:
                    self.html.add('<tr><td style="white-space: nowrap;">')
                    if census.date is not None:
                        self.html.add(f'{census.date.toLongString()[3:]}</td><td>')
                        if individual.birth.date is not None:
                            self.html.add(f'{individual.getYears(census.date)}')
                    else:
                        self.html.add('</td><td>')
                    self.html.add('</td><td>')
                    if census.place is not None:
                        self.html.add(f'{census.place.toLongString()}')
                    self.html.add('</td><td>')
                    if census.facts is not None:
                        for fact in census.facts:
                            if fact.type == 'OCCU':
                                self.html.add(f'{fact.information}')
                    self.html.add('</td><td>')
                    if census.facts is not None:
                        for fact in census.facts:
                            if fact.type == 'NOTE':
                                if fact.information.startswith('Living with'):
                                    self.html.add(f' {fact.information[11:]}')
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
                    if census.facts is not None:
                        for fact in census.facts:
                            if fact.type == 'OCCU':
                                self.html.add(f' working as a {fact.information}')
                            if fact.type == 'NOTE':
                                if fact.information.startswith('Living with'):
                                    self.html.add(f' living with {fact.information[11:]}')
                    self.html.addLine('. ')

        # Facts.
        if individual.facts is not None:
            for fact in individual.facts:
                if fact.type == 'OCCU':
                    self.html.add(f'{firstCap(individual.heShe())} worked as a')
                    if fact.information[0:1] in 'AEIOU':
                        self.html.add('n')
                    self.html.add(f' {fact.information}')
                elif fact.type == 'EDUC':
                    self.html.add(f'{firstCap(individual.heShe())} was educated at {fact.information}')
                elif fact.type == 'NOTE':
                    self.html.add(f'{firstCap(individual.heShe())} {fact.information}')
                else:
                    # Unknown fact type.
                    self.html.add(f'{fact.type} {fact.information}')
                for source in fact.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
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
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
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
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>{source.title}</h1>')

        isUseStandardRender = True

        if source.title.startswith('Marriage'):
            # Marriage certificate.
            grid = None
            if source.facts is not None:
                for fact in source.facts:
                    if isinstance(fact.information, list):
                        grid = fact.information
            if grid is not None:
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

        elif source.title.startswith('Birth'):
            # Birth Certificate.
            grid = None
            if source.facts is not None:
                for fact in source.facts:
                    if isinstance(fact.information, list):
                        grid = fact.information
            if grid is not None:
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

        elif source.title.startswith('Death'):
            # Death Cerificate.
            grid = None
            if source.facts is not None:
                for fact in source.facts:
                    if isinstance(fact.information, list):
                        grid = fact.information
            if grid is not None:
                try:
                    self.html.addLine('<table class="certificate" style="background-color: thistle; border: 1px solid black;" align=center cellpadding=5 cellspacing=0>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Registration District</span></td><td colspan=3>{grid[1][1]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">When and Where</span></td><td colspan=3>{grid[2][1]}</td></tr>')
                    self.html.add(f'<tr><td style="text-align: right;"><span class="death">Name</span></td><td>{grid[4][1]}</td>')
                    self.html.addLine(f'<td style="text-align: right;"><span class="death">Sex</span></td><td>{grid[4][2]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Date Place of Birth</span></td><td colspan=3>{grid[5][1]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Occupation</span></td><td colspan=3>{grid[6][1]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Usual Address</span></td><td colspan=3>{grid[7][1]}</td></tr>')
                    self.html.addLine(f'<tr><td style="text-align: right;"><span class="death">Cause of Death</span></td><td colspan=3>{grid[8][1]}</td></tr>')
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
            if source.facts is not None:
                for fact in source.facts:
                    if isinstance(fact.information, list):
                        grid = fact.information
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
            if source.facts is not None:
                for fact in source.facts:
                    self.html.addLine(f'<p>{fact.toLongString()}</p>')
        else:
            # Show any extra facts.
            if source.facts is not None:
                for fact in source.facts:
                    if not isinstance(fact.information, list):
                        self.html.addLine(f'<p>{fact.toLongString()}</p>')

        # Show the last change.
        if source.change is not None:
            self.html.addLine(f'<p class="change">Last change {source.change.toLongString()}</p>')

        # Show the people that reference this source.
        self.html.addLine('<p>Individuals</p>')
        self.html.addLine('<table class="reference">')
        for individual in self.application.gedcom.individuals.values():
            facts = ''
            # print(f'{individual.identity} {individual.getName()}')
            if identity in individual.sources:
                facts += ' '
            if identity in individual.nameSources:
                facts += 'Name, '
            if individual.birth is not None:
                if individual.birth.date is not None:
                    if identity in individual.birth.date.sources:
                        facts += 'Birth Date, '
                if individual.birth.place is not None:
                    if identity in individual.birth.place.sources:
                        facts += 'Birth Place, '
                if identity in individual.birth.sources:
                    facts += 'Birth, '
            if individual.death is not None:
                if individual.death.date is not None:
                    if identity in individual.death.date.sources:
                        facts += 'Death Date, '
                if individual.death.place is not None:
                    if identity in individual.death.place.sources:
                        facts += 'Death Place, '
                if identity in individual.death.sources:
                    facts += 'Death, '
            if facts != '':
                self.html.addLine(f'<tr><td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td><td>{facts[:-2]}</td></tr>')
        self.html.addLine('</table>')

        # Show the families that reference this source.
        self.html.addLine('<p>Families</p>')
        self.html.addLine('<table class="reference">')
        for family in self.application.gedcom.families.values():
            facts = ''
            if family.marriage is not None:
                if family.marriage.date is not None:
                    if identity in family.marriage.date.sources:
                        facts += 'Marriage Date, '
                if family.marriage.place is not None:
                    if identity in family.marriage.place.sources:
                        facts += 'Marriage Place, '
            if family.divorce is not None:
                if identity in family.divorce.sources:
                    facts += 'Divorce, '
                if family.divorce.date is not None:
                    if identity in family.divorce.date.sources:
                        facts += 'Divorce Date, '

            if facts != '':
                self.html.addLine(f'<tr><td><a href="app:family?id={family.identity}">{family.getName()}</a></td><td>{facts[:-2]}</td></tr>')
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
