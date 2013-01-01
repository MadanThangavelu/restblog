# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/directives/restblogheader.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.24 lartola    Initial working version
#


'''
The restblog directive.

Usage::

    .. restblog::
        :type: post or page
        :title: string
        :categories: comma-separated list of strings
        :tags: comma-separated list of strings
        :publish: yes or no
        :id: integer
        :source: yes or no

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import os
from xml.etree import ElementTree

from docutils import nodes
from docutils.parsers.rst import directives 
from docutils.parsers.rst import Directive


class RestBlogHeader( Directive ):

    required_arguments = 0
    optional_arguments = 0
    has_content = False
    final_argument_whitespace = False

    def yesOrNo( value ):
        return directives.choice( value, ( 'yes', 'no', ) )

    def postType( value ):
        return directives.choice( value, ( 'post', 'page', ) )

    option_spec = dict(
        type=postType,
        title=directives.unchanged_required,
        categories=directives.unchanged,
        tags=directives.unchanged,
        publish=yesOrNo,
        id=directives.positive_int,
        source=yesOrNo,
    )


    def run( self ):
        elements = []
        elements += self.getMetadata()
        if self.options.get( 'source', 'no' ) == 'yes':
            elements += self.getSource()
            elements += self.getSourceViewer()
        contents = '\n'.join( elements )
        return [ nodes.raw( '', contents, format='html' ) ]


    def getMetadata( self ):
        metadata = ElementTree.Element(
            'div',
            name='restblogmetadata',
            id='restblogmetadata',
            style='display: none',
        )
        '''
        post = ElementTree.Element(
            'post',
            type=self.options.get( 'type', 'post' ),
            title=self.options.get( 'title', '' ),
            categories=self.options.get( 'categories', '' ),
            tags=self.options.get( 'tags', '' ),
            publish=self.options.get( 'publish', 'yes' ),
            id=str( self.options.get( 'id', 0 ) ),
            source=self.options.get( 'source', 'no' ),
        )
        '''
        post = ElementTree.Element(
            'post',
            type=self.options.get( 'type', 'post' ),
            title=self.options.get( 'title', '' ),            
            tags=self.options.get( 'tags', '' ),
            publish=self.options.get( 'publish', 'yes' ),
            id=str( self.options.get( 'id', 0 ) ),
            source=self.options.get( 'source', 'no' ),
        )

        metadata.text = ElementTree.tostring( post )
        elements = [ ElementTree.tostring( metadata ) ]
        return elements


    def getSource( self ):
        file_name = os.getenv( 'RESTBLOG_SOURCE_FILE_NAME' )
        source = ElementTree.Element(
            'div',
            name='restblogsource',
            id='restblogsource',
            style='display: none',
        )
        preformatted = ElementTree.SubElement( source, 'pre' )
        if file_name:
            file = open( file_name, 'r' )
            text = ''.join( file.readlines() )
            preformatted.text = text
        elements = [ ElementTree.tostring( source ) ]
        return elements


    def getSourceViewer( self ):
        javascript = ElementTree.Element(
            'script',
            language='javascript',
        )
        javascript.text = '''
function restblogToggleSource() {
    source = document.getElementById( "restblogsource" );
    toggle = document.getElementById( "restblogsourcetoggle" );
    if ( source.style.display == "none" ) {
        source.style.display = "block";
        toggle.innerHTML = "hide";
    } else {
        source.style.display = "none";
        toggle.innerHTML = "show";
    }
}
        '''
        toggle = ElementTree.Element(
            'a',
            name='restblogsourcetoggle',
            id='restblogsourcetoggle',
            href='javascript:restblogToggleSource()',
        )
        toggle.text = 'show';
        elements = [
            ElementTree.tostring( javascript ),
            ElementTree.tostring( toggle ),
        ]
        return elements


directives.register_directive( 'restblog', RestBlogHeader )


