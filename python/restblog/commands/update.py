# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/update.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.30 lartola    Initial working version
#


'''
Implements the ``restblog update`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


from optparse import OptionParser
import os

from restblog import post
from restblog import server


USAGE = '''
restblog update [options] <file_name>

Updates the post in the blog with the contents of `file_name` for the post
matching the ``:id:`` option in the ``.. restblog::` directive in `file_name`.

Arguments:
  file_name         A reStructuredText file.
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
    parser.add_option( '-i', '--interactive', action='store_true', help='Prompt for missing credentials when connecting to the server.' )
    options, arguments = parser.parse_args( arguments )

    # Validate

    if not arguments:
        raise RuntimeError, 'Required arguments are missing.'
    count = len( arguments )
    if count != 1:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )

    # Execute

    file_name = arguments[0]
    update( file_name, options.interactive )


def update( file_name, interactive=False ):
    '''update( file_name, interactive=False )

    Formats and updates a post in a restblog from the given `file_name`.

    Parameters:
    - file_name     Input file name with a post written in reStructuredText.
    - interactive   Prompts for missing credentials if set to True. False by
                    default.
    '''

    try:
        html_file_name = post.createFormattedPost( file_name )
        metadata, contents = post.getPostContents( html_file_name )
        
        id = int( metadata.attrib[ 'id' ] )
        publish = metadata.attrib.get( 'publish', 'yes' ) == 'yes'
        blog = server.connect( interactive=interactive )
        if metadata.attrib[ 'type' ] == 'page':
            success = blog.editPage( id, contents, publish=publish )
        else:
            success = blog.editPost( id, contents, publish=publish )
        if not success:
            raise RuntimeError, 'Unexpected error when updating post'
    except Exception, ex:
        print 'Unable to update restblog post from file %(file_name)s. Error: %(ex)s' % locals()
    finally:
        os.remove( html_file_name )


