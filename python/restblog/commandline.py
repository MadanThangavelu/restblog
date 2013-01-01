# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commandline.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.24 lartola    Initial working version
#


'''
Command-line interface to restblog.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import glob
import imp
from optparse import OptionParser
import os

from logger import logger


def getCommandsRoot():
    '''getCommandsRoot() -> str

    Returns absolute path to the ``commands`` directory inside the ``restblog``
    package. Note that this is *not* a Python subpackage, it is just a plain
    *directory*.
    '''

    root = os.path.dirname( __file__ )
    directory = os.path.join( root, 'commands' )
    return directory


def getCommandNames():
    '''getCommandNames() -> list

    Returns a list of string with then names of all the subcommands available
    for the ``restblog`` executable. Subcommands are simple Python modules
    inside the ``restblog/commands`` *directory*.
    '''

    root = getCommandsRoot()
    pattern = os.path.join( root, '*.py' )
    files = glob.glob( pattern )
    names = []
    for file in files:
        name, extension = os.path.splitext( os.path.basename( file ) )
        if name != 'restblog':
            names.append( name )
    return names


def loadCommandByName( name ):
    '''loadCommandByName( name ) -> module

    Locates and imports a restblog subcommand by the given `name`.

    Subcommands can be imported programmatically like this::

        >>> import restblog.commandline
        >>> command = restblog.commandline.loadCommandByName( 'list' )
        >>> command.run( '--last=10' )

    Returns a module object.
    '''

    root = getCommandsRoot()
    file, file_name, description = imp.find_module( name, [ root ] )
    module = imp.load_module( name, file, file_name, description )
    return module


def run( arguments ):
    '''run( arguments )

    Parses and executes the given command-line `arguments`.

    Parameters:

    - arguments: A list of strings representing the command-line arguments
      to the ``restblog`` executable, e.g. ``sys.argv[1:]``
    '''

    names = getCommandNames()
    if arguments and arguments[0] in names:
        # We are invoking a subcommand, e.g. restblog list
        name = arguments[0]
        arguments = arguments[1:]
    else:
        # Running main command by itself, i.e. restblog
        name = 'restblog'

    try:
        command = loadCommandByName( name )
        command.run( arguments )
    except Exception, ex:
        logger.error( 'Unable to execute %(name)s command.', locals() )
        logger.error( 'Details: %(ex)s', locals() )
        print 'Type \'restblog %(name)s --help\' for usage.' % locals()
 

