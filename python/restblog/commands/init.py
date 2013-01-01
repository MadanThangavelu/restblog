# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/init.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.28 lartola    Initial working version
#


'''
Implements the ``restblog init`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


import getpass
from optparse import OptionParser
import os
from xml.etree import ElementTree


USAGE = '''
restblog create [options] <directory> <url> <user>

Initializes a directory as a post repository for the given blog.

Arguments:
  directory     Target directory. Creates it if it doesn't exist.
  url           Address of the blog XMLRPC service.
  user          User account.
'''


def run( arguments ):
    '''run( arguments )

    Parses and executes the given command-line `arguments`.

    Parameters:
    - arguments     A list of strings representing the command-line arguments
                    to ``restblog <command>``, e.g. ``sys.argv[2:]``
    '''

    # Parse

    usage = USAGE.strip()
    parser = OptionParser( usage=usage )
    options = dict(
        interactive=False,
    )
    parser.set_defaults( **options )
    parser.add_option( '-i', '--interactive', action='store_true', help='Prompt for password to be stored in the configuration file. By default, every restblog command will prompt for password.' )
    options, arguments = parser.parse_args( arguments )

    # Validate

    if not arguments:
        raise RuntimeError, 'Required arguments are missing.'
    count = len( arguments )
    if count < 3:
        raise RuntimeError, 'Missing arguments'
    if count > 3:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )

    # Execute

    root, url, user = arguments
    create( root, url, user, options.interactive )


def create( root, url, user, interactive ):
    '''create( root, url, user, interactive )

    Initializes a restblog repository in the given `root` directory.

    Parameters:
    - root          A local directory. Creates it if it does not already exists.
    - url           Address of the blog XMLRPC service.
    - user          User account.
    - interactive   Prompts for missing credentials if set to True. False by
                    default.

    Exceptions:
    Raises a RuntimeError if the directory is already a restblog repository.
    '''

    # Complete credentials as needed

    if interactive:
        password = getpass.getpass( 'Password: ' )

    # Validate and create directories as needed

    root = os.path.abspath( root )
    if not os.path.exists( root ):
        os.mkdir( root )
    directory = os.path.join( root, '.restblog' )
    if os.path.exists( directory ):
        raise RuntimeError, 'Directory %(root)s appears to be an existing restblog repository.' % locals()
    os.mkdir( directory )

    # Prepare a configuration file

    restblog = ElementTree.Element( 'restblog' )
    attributes = dict(
        url=url,
        user=user,
    )
    if interactive:
        attributes[ 'password' ] = password
    server = ElementTree.SubElement( restblog, 'server', **attributes )
    configuration = '\n'.join( [
        '<?xml version="1.0"?>',
        ElementTree.tostring( restblog ),
        '',
    ] )

    # Write configuration file

    file_name = os.path.join( directory, 'restblog.xml' )
    file = open( file_name, 'w' )
    file.write( configuration )
    file.close()


