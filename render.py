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
            'individual'        : self.showIndividual
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
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine("<h1>Home</h1>")
        self.html.addLine("<p>Hello World</p>")
        self.html.addLine('<div style="border: 1px solid black; width: 500px; height: 300px;">')
        self.html.addLine(f'<svg style="vertical-align: top; border: 1px solid black; width: 400px; height: 200px;" xmlns="http://www.w3.org/2000/svg" version="1.1">')
        self.html.addLine('<line x1="0" y1="0" x2="100" y2="100" stroke="red"  stroke-width="3" />')
        self.html.addLine('</svg>')
        self.html.addLine('</div>')
        self.html.addLine("<p>More Hello World</p>")
        individual = self.application.gedcom.individuals[self.application.gedcom.defaultIdentity]
        self.html.addLine('<p>')
        self.html.addLine(f'<a href="app:individual?person={individual.identity}">{individual.getName()}</a> was born {individual.birthDate.toLongString()}')
        self.html.addLine('</p>')



    def showIndividual(self, parameters):
        ''' Show an individual. '''
        identity = parameters['person'] if 'person' in parameters else None

        individual = self.application.gedcom.individuals[identity]

        parentFamily = None
        if individual.parentFamilyIdentity is not None:
            parentFamily = self.application.gedcom.families[individual.parentFamilyIdentity]

        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)
        self.html.addLine(f"<h1>{individual.getName()}</h1>")
        self.html.addLine('<p>')
        self.html.addLine(f'<a href="app:individual?person={individual.identity}">{individual.getName()}</a> was born {individual.birthDate.toLongString()}.')

        if individual.deathDate is not None:
            self.html.addLine(f'{firstCap(individual.heShe())} died {individual.deathDate.toLongString()}</a>.')

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
                    self.html.add(f'{firstCap(family.startDate.toLongString())} {individual.heShe()}')
                else:
                    self.html.add(f'{firstCap(individual.heShe())}')
                self.html.addLine(f' married <a href="app:individual?person={partner.identity}">{partner.getName()}</a>.')

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



    def showIndex(self, _parameters):
        ''' Render the index page. '''
        self.html.clear()
        self.displayToolbar(True, None, None, None, False, False, False, '', self.host)

        self.html.addLine("<h1>Index</h1>")
        self.html.addLine("<ul>")
        self.html.addLine(f'<li><a href="{self.host}list_champions">List of World Champions</a></li>')
        self.html.addLine(f'<li><a href="{self.host}table_drivers">Table of Drivers</a></li>')
        self.html.addLine(f'<li><a href="{self.host}table_teams">Table of Team Grand Prix Wins</a></li>')
        self.html.addLine(f'<li><a href="{self.host}table_country">Table of Driver Nationality</a</li>')
        self.html.addLine(f'<li><a href="{self.host}table_tracks">Table of Tracks</a></li>')
        self.html.addLine(f'<li><a href="{self.host}table_hosts">Table of Hosting Nations</a></li>')
        # self.html.addLine('<li><a href="app:table_driver_seasons">Table of Drivers by Season</a></li>')

        self.html.addLine(f'<li><a href="{self.host}preferences">Preferences</a></li>')
        self.html.addLine(f'<li><a href="{self.host}repair_db">Database Maintainace</a></li>')
        self.html.addLine("</ul>")

        # Set the page flags.
        self.levels = None

