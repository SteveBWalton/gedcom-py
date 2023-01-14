# -*- coding: utf-8 -*-

'''
Module to render pages for the gedcom-py program.
This module implements the :py:class:`Render` class.
'''

# System libraries.
# import sys
import datetime
import time

# The program libraries.
import walton.html
import walton.toolbar



def firstCap(text):
    ''' Returns the text with the first character capitalised. '''
    return text[:1].upper() + text[1:]



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
            'source'            : self.showSource
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
        self.showIndividual({'person': self.application.gedcom.defaultIdentity})



    def showIndex(self, _parameters):
        ''' Render the index page. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)

        self.html.addLine("<h1>Index</h1>")
        self.html.addLine("<ul>")
        self.html.addLine("</ul>")



    def addLocalSource(self, localSources, source):
        ''' Add the specified source to the local sources. '''
        if not source in localSources:
            localSources.append(source)
        return localSources.index(source) + 1



    def displayLocalSources(self, localSources):
        ''' Display the local sources in a table. '''
        if len(localSources) == 0:
            return

        self.html.addLine('<table class="reference">')
        index = 1
        for sourceIdentity in localSources:
            self.html.add(f'<tr><td>{index}</td><td>')
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
        self.html.addLine(f'<text font-size="7pt" text-anchor="middle" x="{x+75}" y="{y+10}">{individual.getName()}</text>')

        # Draw the information.
        if individual.birthDate is not None:
            self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+25}">b. {individual.birthDate.toShortString()}</text>')
        if individual.birthPlace is not None:
            self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+35}">b. {individual.birthPlace.toShortString()}</text>')
        if individual.deathDate is not None:
            self.html.addLine(f'<text font-size="7pt" text-anchor="left" x="{x+10}" y="{y+45}">d. {individual.deathDate.toShortString()}</text>')



    def drawSmallTree(self, identity):
        ''' Draw a small family tree for the specified person. '''

        # Setup a grid to add people to.
        rows = [ [], [], [], [] ]

        # Add this person to the second row.
        rows[2].append(identity)

        # Family details.
        individual = self.application.gedcom.individuals[identity]
        for familyIdentity in individual.familyIdentities:
            family = self.application.gedcom.families[familyIdentity]
            if family.wifeIdentity is not None:
                if family.wifeIdentity != identity:
                    rows[2].append(family.wifeIdentity)
            if family.husbandIdentity is not None:
                if family.husbandIdentity != identity:
                    rows[2].insert(0, family.husbandIdentity)

            for childIdentity in family.childrenIdentities:
                rows[3].append(childIdentity)

        # Parents family.
        if individual.parentFamilyIdentity is not None:
            parentFamily = self.application.gedcom.families[individual.parentFamilyIdentity]
            if parentFamily.husbandIdentity is not None:
                rows[1].append(parentFamily.husbandIdentity)
                father = self.application.gedcom.individuals[parentFamily.husbandIdentity]
                if father.parentFamilyIdentity is not None:
                    fatherFamily = self.application.gedcom.families[father.parentFamilyIdentity]
                    if fatherFamily.husbandIdentity is not None:
                        rows[0].append(fatherFamily.husbandIdentity)
                    if fatherFamily.wifeIdentity is not None:
                        rows[0].append(fatherFamily.wifeIdentity)
            if parentFamily.wifeIdentity is not None:
                rows[1].append(parentFamily.wifeIdentity)
                mother = self.application.gedcom.individuals[parentFamily.wifeIdentity]
                if mother.parentFamilyIdentity is not None:
                    motherFamily = self.application.gedcom.families[mother.parentFamilyIdentity]
                    if motherFamily.husbandIdentity is not None:
                        rows[0].append(motherFamily.husbandIdentity)
                    if motherFamily.wifeIdentity is not None:
                        rows[0].append(motherFamily.wifeIdentity)
        width = 0
        # Decide the required width.
        for columns in rows:
            requiredWidth = len(columns) * 170 - 10
            if requiredWidth > width:
                width = requiredWidth

        # Draw the people.
        self.html.addLine(f'<svg style="vertical-align: top; border: 1px solid black; width: {width}px; height: 270px;" xmlns="http://www.w3.org/2000/svg" version="1.1">')
        y = 5
        for columns in rows:
            x = 5
            for cell in columns:
                self.drawIndividual(cell, x, y)
                x += 170
            y += 70
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
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f"<h1>{individual.getName()}</h1>")

        # Draw a small family tree for the person.
        self.drawSmallTree(identity)

        # Person Description.
        self.html.addLine('<p>')

        # Born details.
        self.html.add(f'<a href="app:individual?person={individual.identity}">{individual.getName()}</a>')
        if len(individual.nameSources) > 0:
            for source in individual.nameSources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        self.html.add(f' was born {individual.birthDate.toLongString()}')
        if len(individual.birthDate.sources) > 0:
            for source in individual.birthDate.sources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        if individual.birthPlace is not None:
            self.html.add(f' at {individual.birthPlace.toLongString()}')
            if len(individual.birthPlace.sources) > 0:
                for source in individual.birthPlace.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
        self.html.addLine('.')

        # Family details.
        for familyIdentity in individual.familyIdentities:
            partner = None
            family = self.application.gedcom.families[familyIdentity]
            if family.wifeIdentity is not None:
                if family.wifeIdentity != identity:
                    partner = self.application.gedcom.individuals[family.wifeIdentity]
            if family.husbandIdentity is not None:
                if family.husbandIdentity != identity:
                    partner = self.application.gedcom.individuals[family.husbandIdentity]
            if partner is not None:
                if family.startDate is not None:
                    self.html.add(f'{firstCap(family.startDate.toLongString())}')
                    for source in family.startDate.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                    self.html.add(f' {individual.heShe()}')
                else:
                    self.html.add(f'{firstCap(individual.heShe())}')
                self.html.add(f' married <a href="app:individual?person={partner.identity}">{partner.getName()}</a>')
                if family.startPlace is not None:
                    self.html.add(f' at {family.startPlace.toLongString()}')
                    for source in family.startPlace.sources:
                        self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
                self.html.addLine('.')

            if len(family.childrenIdentities) == 0:
                self.html.addLine(f'They had no children.')
            else:
                if len(family.childrenIdentities) == 1:
                    self.html.add(f'They had 1 child')
                else:
                    self.html.add(f'They had {len(family.childrenIdentities)} children')
                for childIdentity in family.childrenIdentities:
                    child = self.application.gedcom.individuals[childIdentity]
                    self.html.add(f', <a href="app:individual?person={child.identity}">{child.getName()}</a>')
                self.html.addLine('.')

        # Death details.
        if individual.deathDate is not None:
            self.html.add(f'{firstCap(individual.heShe())} died {individual.deathDate.toLongString()}</a>')
            for source in individual.deathDate.sources:
                self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
            if individual.deathPlace is not None:
                self.html.add(f' at {individual.deathPlace.toLongString()}')
                for source in individual.deathPlace.sources:
                    self.html.add(f'<sup>{self.addLocalSource(localSources, source)}</sup>')
            self.html.addLine('.')

        # Parents details.
        if parentFamily is not None:
            father = None
            if parentFamily.husbandIdentity is not None:
                father = self.application.gedcom.individuals[parentFamily.husbandIdentity]
            mother = None
            if parentFamily.wifeIdentity is not None:
                mother = self.application.gedcom.individuals[parentFamily.wifeIdentity]

            if father is not None and mother is not None:
                self.html.addLine(f'{firstCap(individual.hisHer())} parents were <a href="app:individual?person={father.identity}">{father.getName()}</a> and <a href="app:individual?person={mother.identity}">{mother.getName()}</a>.')

        self.html.addLine('</p>')

        # Add the sources that have not been used.
        for source in individual.sources:
            self.addLocalSource(localSources, source)

        # Display the sources referenced in this document.
        self.displayLocalSources(localSources)



    def showSource(self, parameters):
        ''' Show an individual. '''
        identity = parameters['id'] if 'id' in parameters else None

        source = self.application.gedcom.sources[identity]

        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f'<h1>{source.title}</h1>')

        if source.title.startswith('Marriage'):
            # Marriage certificate.
            grid = source.note.getGrid()
            self.html.addLine('<table class="certificate" style="background-color: #ccff99; border: 1px solid black;" align="center" cellpadding="5" cellspacing="5">')
            self.html.add('<tr><td colspan="7">')
            if source.date is not None:
                self.html.add(source.date.theDate.strftime("%Y"))
            self.html.add(' <span class="marriage">Marriage solemnized at</span> ')
            if source.place is not None:
                self.html.add(source.place.toLongString())
            self.html.addLine('</td></tr>')
            self.html.add('<tr>')
            self.html.add('<td><SPAN class=\"marriage\">When Married</SPAN></td>')
            self.html.add('<td><SPAN class=\"marriage\">Name</SPAN></td>')
            self.html.add('<td><SPAN class=\"marriage\">Age</SPAN></td>')
            self.html.add('<td><SPAN class=\"marriage\">Rank or Profession</SPAN></td>')
            self.html.add('<td><SPAN class=\"marriage\">Residence at the time of marriage</SPAN></td>')
            self.html.add('<td><SPAN class=\"marriage\">Father\'s Name</SPAN></td>')
            self.html.add('<td><SPAN class=\"marriage\">Rank of Profession of Father</SPAN></td>')
            self.html.addLine('</tr>')
            self.html.add("<tr>")
            self.html.add('<td rowspan=2 style="white-space: nowrap;">')
            if source.date is not None:
                self.html.add(source.date.theDate.strftime("%-d %b %Y"))
            # when.ToString("d MMM yyyy")
            self.html.add('</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[1][1]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[1][2]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[1][3]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[1][4]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[3][1]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[3][2]}</td>')
            self.html.addLine('</tr>')
            self.html.add('<tr>')
            #// sbHtml.Append("<TD><SPAN class=\"Small\">Bride</SPAN></TD>")
            self.html.add(f'<td style="white-space: nowrap;">{grid[2][1]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[2][2]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[2][3]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[2][4]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[4][1]}</td>')
            self.html.add(f'<td style="white-space: nowrap;">{grid[4][2]}</td>')
            self.html.addLine('</tr>')
            self.html.addLine(f'<tr><td colspan="7"><span class="marriage">in the Presence of us,</span> {grid[5][1]}</td></tr>')
            self.html.add('<tr><td colspan=7 align=center><span class="marriage">GRO Reference</span> ')
            self.html.add(grid[0][1])
            self.html.addLine('</td></tr>')
            self.html.addLine('</table>')
        elif source.title.startswith('Birth'):
            # Birth Certificate.
            grid = source.note.getGrid()
            self.html.addLine('<table class="certificate" style="background-color: mistyrose; border: 1px solid black;" align="center" cellpadding="5" cellspacing="0">')
            self.html.add('<tr><td colspan="8">')
            if source.date is not None:
                self.html.add(source.date.theDate.strftime("%Y"))
            self.html.addLine(f' <span class="birth">Birth in the registration district of</span> {grid[1][1]}</td></tr>')
            self.html.add('<tr valign="bottom"><td><span class="birth">When and<br/>Where Born</span></td>')
            self.html.add('<td class="birth">Name</td>')
            self.html.add('<TD><SPAN class="birth">Sex</SPAN></TD>')
            self.html.add('<TD><SPAN class="birth">Father</SPAN></TD>')
            self.html.add('<TD><SPAN class="birth">Mother</SPAN></TD>')
            self.html.add('<TD><SPAN class="birth">Occupation<BR>of Father</SPAN></TD>')
            self.html.add('<TD><SPAN class="birth">Informant</SPAN></TD>')
            self.html.addLine('<TD><SPAN class="birth">When Registered</SPAN></TD></TR>')

            self.html.add('<TR valign=top><TD>')
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
            self.html.add(f'<tr><td colspan="8" align="center"><span class="birth">GRO Reference</span> {grid[0][1]}</td></tr>')
            self.html.add('</table>');

            # Debugging.
            self.html.addLine('<table>')
            for rows in grid:
                self.html.add('<tr>')
                for cell in rows:
                    self.html.add(f'<td style="white-space: nowrap;">\'{cell}\'</td>')
                self.html.addLine('</tr>')
            self.html.addLine('</table>')
        else:
            # General source.
            if source.date is not None:
                self.html.addLine(f'<p>{source.date.toLongString()}</p>')
            if source.note is not None:
                for line in source.note.lines:
                    self.html.addLine(f'<p>{line}</p>')

                # Debugging.
                grid = source.note.getGrid()
                self.html.addLine('<table>')
                for rows in grid:
                    self.html.add('<tr>')
                    for cell in rows:
                        self.html.add(f'<td style="white-space: nowrap;">\'{cell}\'</td>')
                    self.html.addLine('</tr>')
                self.html.addLine('</table>')

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
            if individual.birthDate is not None:
                if identity in individual.birthDate.sources:
                    facts += 'Birth Date, '
            if individual.birthPlace is not None:
                if identity in individual.birthPlace.sources:
                    facts += 'Birth Place, '
            if individual.deathDate is not None:
                if identity in individual.deathDate.sources:
                    facts += 'Death Date, '
            if individual.deathPlace is not None:
                if identity in individual.deathPlace.sources:
                    facts += 'Death Place, '
            if facts != '':
                self.html.addLine(f'<tr><td><a href="app:individual?id={individual.identity}">{individual.getName()}</a></td><td>{facts[:-2]}</td></tr>')
        self.html.addLine('</table>')

        # Show the families that reference this source.
        self.html.addLine('<p>Families</p>')
        self.html.addLine('<table class="reference">')
        for family in self.application.gedcom.families.values():
            facts = ''
            if family.startDate is not None:
                if identity in family.startDate.sources:
                    facts += 'Marriage Date, '
            if family.startPlace is not None:
                if identity in family.startPlace.sources:
                    facts += 'Marriage Place, '

            if facts != '':
                self.html.addLine(f'<tr><td><a href="app:family?id={family.identity}">{family.identity}</a></td><td>{facts[:-2]}</td></tr>')
        self.html.addLine('</table>')
