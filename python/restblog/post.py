# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/post.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.30 lartola    Initial working version
#


'''
Functions to transform and manipulate a restblog post from XHTML.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import os
import subprocess
import tempfile
from xml.etree import ElementTree

import restblog2html


def createFormattedPost( file_name ):
    '''createFormattedPost( file_name ) -> str

    Translates the given `file_name` into an XHTML document.

    Parameters:

    - file_name: Input file with a post in reStructuredText format.

    Returns the name of a file with the XHTML document.
    '''

    output_file, output_file_name = tempfile.mkstemp( prefix='restblog_', suffix='.html' )
    os.close( output_file )
    arguments = [ file_name, output_file_name ]
    restblog2html.main( arguments )
    return output_file_name


def getPostContents( file_name ):
    '''getPostContents( file_name ) -> ( `xml.etree.ElementTree.Element`, dict )

    Extracts the relevant portions of the post from the given XHTML `file_name`.

    Parameters:
    
    - file_name: Name of the XHTML input file name.

    Returns a tuple with the following values:

    - An `xml.etree.ElementTree.Element` that contains the post metadata. This is
      basically the options extracted from the ``.. restblog::`` directive
      stored in the input reStructuredText file used to produce the given XHTML
      `file_name`. See `restblog.directives.restblogheader` for more information.

    - A dictionary with the actual portion of the XHTML document that contains
      the post contents. Contains the following keys:
            
        - title: str
        - description: str
        - mt_excerpt: str
        - mt_text_more: str
        - mt_keywords: list
        - categories: list

    '''

    # The input XHTML as generated by restblog uses namespaces
    namespace = 'http://www.w3.org/1999/xhtml'
    body_tag = str( ElementTree.QName( namespace, 'body' ) )
    div_tag = str( ElementTree.QName( namespace, 'div' ) )

    # Parse document for tearing it apart easily
    document = ElementTree.parse( file_name )
    body = document.find( body_tag )

    # Find tags with special meaning for restblog
    nodes = document.getiterator( div_tag )
    metadata_node = None
    full_story_sentinel = None
    full_story_sentinel_index = 0
    for index, node in enumerate( nodes ):
        if node.attrib.get( 'name' ) == 'restblogmetadata':
            metadata_node = node
        elif node.attrib.get( 'name' ) == 'restblogfullstory':
            full_story_sentinel = node
            full_story_sentinel_index = index
    if metadata_node is None:
        raise RuntimeError, 'Unable to find restblog metadata in the formated post.'
    metadata = ElementTree.XML( metadata_node.text )

    # Extract actual contents of the post
    title = metadata.attrib.get( 'title' )
    if not title:
        name, extension = os.path.splitext( os.path.basename( file_name ) )
        title = name
    categories = metadata.attrib.get( 'categories', [] )
    if categories:
        categories = map( str.strip, categories.split( ',' ) )
    tags = metadata.attrib.get( 'tags', [] )
    if tags:
        tags = map( str.strip, tags.split( ',' ) )

    
    # Translate XHTML portions we actually care about
    body = body.find( div_tag )
    removeLineBreaksFromElement( body )
    if metadata_node is not None:
        body.remove( metadata_node )
    if full_story_sentinel is not None:
        comment = ElementTree.Comment( 'more' )
        body.insert( full_story_sentinel_index, comment )
        body.remove( full_story_sentinel )
    post = ElementTree.tostring( body )

    # Remove any namespace notation from tags and translate special tags
    post = post.replace( '<html:', '<' )
    post = post.replace( '</html:', '</' )
    post = post.replace( '<!-- more -->', '<!--more-->' )
    post = post.strip()

    # Build contents as expected by the metaWeblog.newPost API method
    '''
    contents = dict(
        title=title,
        description=post,
        mt_excerpt='',
        mt_text_more='',
        mt_keywords=tags,
        categories=categories,
    )
    '''
    contents = dict(
        title=title,
        description=post,
        mt_excerpt='',
        mt_text_more='',
        mt_keywords=tags,    
    )

    return metadata, contents
    

def removeLineBreaksFromElement( element ):
    '''removeLineBreaksFromElement( element )

    Removes line breaks from text in paragraphs that is not preformatted.
    For some reason, Wordpress appears to be - incorrectly IMHO, replacing
    new-line characters with an actual line break, i.e. <br />

    Needless to say, that just goes against what straight HTML would do,
    i.e. text in paragraphs does not respect line breaks and it's rendered
    as one contiguous line, e.g.::

        <p>one
        two three
        four five six</p>

    Should be rendered as::

        one two three four five six

    Not::

        one<br />
        two three<br />
        four five six

    Simply because it is a <p/> element not <pre/>.

    In any event, this function removes all line breaks and turns multiline
    paragraphs into a single running line of text.

    Parameters:

    - element: An `xml.etree.ElementTree.Element` whose text will be stripped
      off new-line characters.
    '''

    def removeLineBreaks( text ):
        if text is None:
            return text
        lines = text.split( '\n' )
        text = ' '.join( lines )
        return text

    namespace = 'http://www.w3.org/1999/xhtml'
    p_tag = str( ElementTree.QName( namespace, 'p' ) )
    paragraphs = element.findall( p_tag )
    for paragraph in paragraphs:
        paragraph.text = removeLineBreaks( paragraph.text )
        paragraph.tail = removeLineBreaks( paragraph.tail )
        for child in paragraph.getchildren():
            child.text = removeLineBreaks( child.text )
            child.tail = removeLineBreaks( child.tail )


def updateSourceMetadata( file_name, metadata ):
    '''updateSourceMetadata( file_name, metadata )

    Parameters:

    - file_name: File to the source post in reStructuredText to be updated.
    - metadata: An `xml.etree.ElementTree.Element` representing all the values
      that describe a post. This maps to all the options to the
      ``.. restblog::`` directive.
    '''

    before, restblog, after = splitSourceAtRestblogDirective( file_name )
    restblog = buildRestblogFromMetadata( metadata )
    lines = before + restblog + after
    file = open( file_name, 'w' )
    file.writelines( lines )
    file.close()


def splitSourceAtRestblogDirective( file_name ):
    '''splitSourceAtRestblogDirective( file_name ) -> ( list, list, list )

    Locates the block containing a ``.. restblog::`` directive and splits
    the contents. Returns the block of lines before, the restblog block and
    the lines after it.

    I'm sure there is a better way, but given the structure of a
    reStructuredText document, let's take a naive approach and scan the file
    to update the lines starting with ``.. restblog::`` and the contiguous lines
    before an empty line with the given metadata, e.g.::
    
        .. restblog::
           :title: Some title here
           :source: yes

    Parameters:

    - file_name: File to the source post in reStructuredText to split.

    Returns a tuple of three lists with the lines before the directive, the
    directive itself and after it.
    '''
    
    file = open( file_name, 'r' )
    lines = file.readlines()
    file.close()

    before = []
    restblog = []
    after = []

    extracting = False

    for index, line in enumerate( lines ):
        if not extracting:
            if '.. restblog::' in line:
                extracting = True
                restblog.append( line )
            else:
                before.append( line )
        else:
            if line.strip():
                restblog.append( line )
            else:
                # we've reached the end of the directive as indicated by an
                # empty line.
                extracting = False
                after = lines[index+1:]
                break

    return before, restblog, after


def buildRestblogFromMetadata( metadata ):
    '''buildRestblogFromMetadata( metadata ) -> list

    Recreates a ``.. restblog::`` directive from the given `metadata`.

    Parameters:

    - metadata: An `xml.etree.ElementTree.Element` with all the values to
      describe a post.

    Returns a list of strings.
    '''

    lines = [ '.. restblog::\n' ]

    for key, value in sorted( metadata.attrib.items() ):
        line = '    :%(key)s: %(value)s\n' % locals()
        lines.append( line )

    lines.append( '\n' )

    return lines

