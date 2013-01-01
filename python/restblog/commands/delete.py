# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/delete.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.24 lartola    Initial working version
#


'''
Implements the ``restblog delete`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


from optparse import OptionParser
import os
from xml.etree import ElementTree

from restblog.logger import logger
from restblog import post
from restblog import server


USAGE = '''
restblog delete [options] <post_id>

Deletes a post from a restblog.

Arguments:
  post_id       Post ID to delete
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
        force=False,
    )
    parser.set_defaults( **options )
    parser.add_option( '-i', '--interactive', action='store_true', help='Prompt for missing credentials when connecting to the server.' )
    parser.add_option( '-f', '--force', action='store_true', help='Force deletion without confirmation' )
    options, arguments = parser.parse_args( arguments )

    # Validate

    if not arguments:
        raise RuntimeError, 'Required arguments are missing.'
    count = len( arguments )
    if count != 1:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )

    # Execute

    post_id = int( arguments[0] )
    delete( post_id, interactive=options.interactive, force=options.force )


def delete( post_id, interactive=False, force=False ):
    '''delete( post_id, interactive=False, force=False )

    Deletes the post with the given `post_id` from a restblog.

    Parameters:

    - post_id: Post ID to delete.
    - interactive: Prompts for missing credentials if set to True. False by
      default.
    - force: Force deletion without confirmation.
    '''

    try:
        blog = server.connect( interactive=interactive )
        if not force:
            prompt = 'Delete post number %(post_id)s? [y/N]: ' % locals()
            confirmed = raw_input( prompt )
            if confirmed.lower() != 'y':
                logger.info( 'Post will not be deleted.' )
                return
        logger.info( 'Deleting post %(post_id)s', locals() )
        blog.deletePost( post_id, publish=True )
        logger.info( 'Done.' )
    except Exception, ex:
        print 'Unable to delete post %(post_id)s from restblog. Error: %(ex)s' % locals()


