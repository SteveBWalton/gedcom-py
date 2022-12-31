#!/bin/bash
#
# Script to set the file permissions in the gedcom-py source code directory.
#

# Make a walton folder for the library modules.
if [ ! -d "walton" ] ; then
    mkdir "walton"
fi
if [ ! -e "walton/__init__.py" ] ; then
    touch "walton/__init__.py"
fi

# Check that the library modules exist.
#if [ ! -e "walton/xml.py" ] ; then
#    ln -s ../../Library/py3/modXml.py walton/xml.py
#fi
if [ ! -e "walton/html.py" ] ; then
    ln -s ../../../Library/py3/modHtml.py walton/html.py
fi
if [ ! -e "walton/install.py" ] ; then
    ln -s ../../../Library/py3/modInstall.py walton/install.py
fi
if [ ! -e "walton/toolbar.py" ] ; then
    ln -s ../../../Library/py3/interfaceToolbar.py walton/toolbar.py
fi
if [ ! -e "walton/application.py" ] ; then
    ln -s ../../../Library/py3/interfaceApplication.py walton/application.py
fi
if [ ! -e "walton/ansi.py" ] ; then
    ln -s ../../../Library/py3/ansi.py walton/ansi.py
fi


# Make a docs folder for the documentation.
if [ ! -d "docs" ] ; then
    mkdir "docs"
fi
if [ ! -e "docs/index.html" ] ; then
    ln -s _build/html/index.html docs/index.html
fi

# Make a Styles folder.
if [ ! -e "Styles" ] ; then
    mkdir Styles
fi

# Set everything in this directory to 600.
chmod 600 * 2> /dev/null

# Directories need execute permission.
chmod 700 $(ls -d */)

# Special files need execute permission.
chmod 700 *.sh
chmod 700 gedcom.py
