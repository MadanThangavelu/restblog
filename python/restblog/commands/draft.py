# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/draft.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.28 lartola    Initial working version
#


'''
Implements the ``restblog draft`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


from optparse import OptionParser
import os


USAGE = '''
restblog draft [options] <file_name>

Creates a skeleton restblog post in reStructuredText format.

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
        title=None,
        type='post',
    )
    parser.set_defaults( **options )
    parser.add_option( '-t', '--title', help='Post title. Use file name if not specified.' )
    parser.add_option( '-p', '--page', dest='type', action='store_const', const='page', help='This is page, not a post.' )
    options, arguments = parser.parse_args( arguments )

    # Validate

    if not arguments:
        raise RuntimeError, 'Required arguments are missing.'
    count = len( arguments )
    if count != 1:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )

    # Execute

    file_name = arguments[0]
    draft( file_name, title=options.title, type=options.type )


def draft( file_name, title, type ):
    '''draft( file_name, title, type )

    Creates a skeleton restblog post file.

    Parameters:
    - file_name     Output file name.
    - title         Post title.
    - type          Post type, i.e. post or page.

    Exceptions:
    Raises an Exception if the `file_name` cannot be written.
    '''

    if not title:
        # Let's use the file name and attempt to turn it into a
        # pretty title, e.g.
        # from: this-is-a-post.rst
        # to: This is a post
        title = os.path.splitext( os.path.basename( file_name ) )[0]
        title = title.capitalize()
        title = title.replace( '-', ' ' )

    contents = '''
.. restblog::
    :title: %(title)s
    :type: %(type)s

.. Replace this line with the contents of your post
''' % locals()

    file = open( file_name, 'w' )
    file.write( contents )
    file.close()


