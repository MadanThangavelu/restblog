# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/restblog.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.28 lartola    Initial working version
#


'''
Implements the main ``restblog`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


from optparse import OptionParser
import os

from restblog.commandline import getCommandNames
from restblog.version import VERSION


USAGE = '''restblog <command> [options] [arguments]

restblog is a tool for creating and editing content in a blog using
reStructuredText. It provides a simple command-line interface, Python
API and plugins for developer text editors such as MacVim.

For additional information go to http://luisartola.com/software/restblog

Available subcommands:
%(command_names)s'''


def run( arguments ):
    '''run( arguments )

    Parses and executes the given command-line `arguments`.

    Parameters:
    - arguments     A list of strings representing the command-line arguments
                    to ``restblog <command>``, e.g. ``sys.argv[1:]``
    '''

    # Parse

    command_names = '\n'.join( getCommandNames() )
    usage = USAGE.strip() % locals()
    parser = OptionParser( usage=usage )
    options = dict(
        version=False,
    )
    parser.set_defaults( **options )
    parser.add_option( '-v', '--version', action='store_true', help='Print version information.' )
    options, arguments = parser.parse_args( arguments )

    # Validate

    if arguments:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )

    # Execute

    if options.version:
        print VERSION
    else:
        parser.print_help()


