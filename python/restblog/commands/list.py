# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/list.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.24 lartola    Initial working version
#


'''
Implements the ``restblog list`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


from optparse import OptionParser
import os

from restblog import server


USAGE = '''
restblog list [options] [url]

Lists basic information about the most recent posts from a blog.

Arguments:
  url     URL to the blog XMLRPC service (optional.) Uses .restblog if not specified.
'''


def run( arguments ):
    usage = USAGE.strip()
    parser = OptionParser( usage=usage )
    options = dict(
        count=10,
        header=False,
        interactive=False,
        user='',
        password='',
    )
    parser.set_defaults( **options )
    parser.add_option( '-l', '--last', dest='count', help='Show only the last number of posts.' )
    parser.add_option( '-e', '--header', action='store_true', help='Show column headers. Hidden by default.' )
    parser.add_option( '-i', '--interactive', action='store_true', help='Prompt for missing credentials when connecting to the server.' )
    parser.add_option( '-u', '--user' )
    parser.add_option( '-p', '--password' )
    options, arguments = parser.parse_args( arguments )
    if len( arguments ) > 1:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )
    url = arguments[0] if arguments else ''
    listPosts(
        url,
        count=int( options.count or 0 ),
        header=options.header,
        user=options.user,
        password=options.password,
        interactive=options.interactive,
    )


def listPosts( url, count, header, user, password, interactive=False ):
    blog = server.connect( url, user=user, password=password, interactive=interactive )
    posts = blog.getRecentPostTitles( count )
    if not posts:
        print 'No posts found.'
        return
    maximum_width = findMaximumWidth( posts, padding=2 )
    format = \
        '%%(postid)%(postid)ds  ' \
        '%%(title)-%(title)ds  ' \
        '%%(restblog_timestamp)-%(restblog_timestamp)ds' \
        % maximum_width
    if header:
        text = format % dict( postid='id', title='title', restblog_timestamp='created' )
        print text
        print '-'*len( text )
    for post in posts:
        postid = post[ 'postid' ]
        title = post[ 'title' ]
        restblog_timestamp = str( post[ 'dateCreated' ] ).replace( 'T', ' ' )
        print format % locals()


def findMaximumWidth( posts, padding ):
    maximum = dict()
    for post in posts:
        def updateMaximumWidth( column, target=None, padding=padding ):
            target = target if target else column
            if target not in maximum:
                maximum[ target ] = 0
            width = len( str( post[ column ] ) ) + padding
            if width > maximum[ target ]:
                maximum[ target ] = width
        updateMaximumWidth( 'postid' )
        updateMaximumWidth( 'title' )
        updateMaximumWidth( 'dateCreated', 'restblog_timestamp' )
    return maximum


