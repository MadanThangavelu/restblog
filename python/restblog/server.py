# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/server.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.27 lartola    Initial working version
#


'''
Encapsulates a connection to a blog server and provides a simplified API to
manage posts and pages.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import getpass
import os
from xml.etree import ElementTree
import xmlrpclib


class Server( object ):
    '''Server( url, user='', password='' ) -> instance

    Provides a simplified API to a subset of methods from the various blogging
    APIs, i.e.  Wordpress, MetaWeblog, Blogger, MoveableType. Manages the
    connection to a blog server using XMLRPC.

    Parameters:

    - url: Address of the XMLRPC blog server, e.g. http://your.blog.com/xmlrpc.php
    - user: Optional user name.
    - password: Optional password.
    '''


    def __init__( self, url, user='', password='' ):
        self.__blog = xmlrpclib.Server( url )
        self.__user = user if user else ''
        self.__password = password if password else ''
        self.__blog_id = 1


    def getRecentPostTitles( self, count=10 ):
        '''getRecentPostTitles( count=10 ) -> list

        Returns a list with minimal information about the most recent posts.

        Encapsulates MoveableType function ``mt.getRecentPostTitles``.

        Parameters:

        - count: Number of posts to retrieve. Default is 10.

        Returns:

        A list of dictionaries representing data from the post. Including
        ``postid``, ``title`` and ``dateCreated``.
        '''

        titles = self.__blog.mt.getRecentPostTitles(
            self.__blog_id, self.__user, self.__password, count
        )
        return titles


    def newPost( self, contents, publish ):
        '''newPost( contents, publish ) -> int

        Creates a new post.

        Encapsulates MetaWeblog function ``metaWeblog.newPost``.

        Parameters:

        - contents: A dictionary with the keys listed below.
            
            - title: str
            - description: str
            - mt_excerpt: str
            - mt_text_more: str
            - mt_keywords: list
            - categories: list

        - publish: Whether to publish immediately or not. Default is True.

        Returns:

        An integer with the post ID just created.
        '''

        id = self.__blog.metaWeblog.newPost(
            self.__blog_id, self.__user, self.__password, contents, publish 
        )
        return id


    def editPost( self, id, contents, publish ):
        '''edit( contents, publish ) -> bool

        Updates the post with the given ``id`` and ``contents``.

        Encapsulates MetaWeblog function ``metaWeblog.editPost``.

        Parameters:

        - contents: A dictionary with the keys listed below.
            
            - title: str
            - description: str
            - mt_excerpt: str
            - mt_text_more: str
            - mt_keywords: list
            - categories: list

        - publish: Whether to publish changes immediately or not.
          Default is True.

        Returns:

        True if the update was successful. False otherwise.
        '''

        success = self.__blog.metaWeblog.editPost(
            id, self.__user, self.__password, contents, publish 
        )
        return success


    def getPost( self, id ):
        '''getPost( id ) -> dict

        Returns the post with the given ``id``.

        Encapsulates MetaWeblog function ``metaWeblog.getPost``.

        Parameters:

        - id: Post ID to return.

        Returns:

        - A dictionary with the keys listed below.
            
            - title: str
            - description: str
            - mt_excerpt: str
            - mt_text_more: str
            - mt_keywords: list
            - categories: list
        '''

        post = self.__blog.metaWeblog.getPost(
            id, self.__user, self.__password
        )
        return post


    def deletePost( self, id, publish ):
        '''deletePost( id, publish ) -> bool

        Deletes post with the given ``id``.

        Encapsulates MetaWeblog function ``metaWeblog.deletePost``.

        Parameters:

        - id: Post ID to delete.
        - publish: Whether to publish the deletion immediately or not.
          Default is True.

        Returns:

        True if the deletion was successful. False otherwise.
        '''

        success = self.__blog.metaWeblog.deletePost(
            '', id, self.__user, self.__password, publish 
        )
        return success


    def newPage( self, contents, publish ):
        '''newPage( contents, publish ) -> int

        Creates a new page. This function is practically identical to
        ``newPost``. It receives the same parameters. One note though,
        ``contents`` may have some extra keys that do not quite apply
        to pages, e.g. tags and categories, but are gracefully ignored
        by the actual implementation on the server side.

        Encapsulates Wordpress function ``wp.newPage``.

        Parameters:

        - contents: A dictionary with the keys described in ``newPost``.
        - publish: Whether to publish immediately or not. Default is True.

        Returns:

        An integer with the page ID just created.
        '''

        id = self.__blog.wp.newPage(
            self.__blog_id, self.__user, self.__password, contents, publish 
        )
        return id


    def editPage( self, id, contents, publish ):
        '''editPage( id, contents, publish ) -> bool

        Edit page with the given ``id``. This function is practically
        identical to ``editPost``. It receives the same parameters.
        One note though, ``contents`` may have some extra keys that do not
        quite apply to pages, e.g. tags and categories, but are gracefully
        ignored by the actual implementation on the server side.

        Encapsulates Wordpress function ``wp.editPage``.

        Parameters:

        - contents: A dictionary with the keys described in ``editPost``.
        - publish: Whether to publish immediately or not. Default is True.

        Returns:

        True if the update was successful. False otherwise.
        '''

        success = self.__blog.wp.editPage(
            self.__blog_id, id, self.__user, self.__password, contents, publish 
        )
        return success


    def ping( self ):
        '''ping()

        Sends a request to the server just to verify that it can log in with
        the credentials given when constructing the ``Server`` instance.

        Raises an exception if the request fails for any reason, including
        bad credentials or simply connection errors.
        '''

        # Verify that we can connect to the server and there are remote methods
        # in the API that can be executed.
        self.__blog.system.listMethods()


def connect( url='', user='', password='', interactive=False ):
    '''connect( url='', user='', password='', interactive=False ) -> Server

    Convenience function to create a ``Server`` object. This is the preferred
    method over constructing a ``Server`` directly. It would attempt to use
    the given credentials if not empty. Otherwise, it would look into the
    *.restblog* directory, if it exists, to extract the default credentials.

    Parameters:

    - url: Address of the XMLRPC blog server, e.g. http://your.blog.com/xmlrpc.php
    - user: Optional user name.
    - password: Optional password.
    - interactive: Prompts user for missing credentials like user and/or
      password when set to True. By default it is set to False meaning that it
      would use the given credentials and fail if it can't connect for any
      reason.

    Returns:

    A ``Server`` instance.
    '''

    # Attempt to extract missing credentials from the .restblog
    # directory first
    file_name = os.path.join( os.getcwd(), '.restblog', 'restblog.xml' )
    if not url and file_name:
        document = ElementTree.parse( file_name )
        restblog = document.getroot()
        server = restblog.find( 'server' )
        url = server.attrib.get( 'url', '' )
        user = server.attrib.get( 'user', '' )
        password = server.attrib.get( 'password', '' )

    # We need a URL at the very least, fail if that's not the case
    if not url:
        raise RuntimeError, 'Please specify a blog URL'

    # Fill in missing credentials if instructed to do so
    if interactive:
        if not user:
            user = raw_input( 'User: ' )
        if not password:
            password = getpass.getpass( 'Password: ' )

    # Attempt a server connection and verify that it works
    try:
        server = Server( url, user, password )
        server.ping()
        return server
    except Exception, ex:
        raise RuntimeError, 'Unable to open connection to %(url)s. Error: %(ex)s' % locals()
    

