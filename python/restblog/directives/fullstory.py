# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/directives/fullstory.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.07.13 lartola    Initial working version
#


'''
The restblog fullstory directive.

Usage::

    .. fullstory::

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import os
from xml.etree import ElementTree

from docutils import nodes
from docutils.parsers.rst import directives 
from docutils.parsers.rst import Directive


class FullStory( Directive ):

    required_arguments = 0
    optional_arguments = 0
    has_content = False
    final_argument_whitespace = False

    def yesOrNo( value ):
        return directives.choice( value, ( 'yes', 'no', ) )

    option_spec = dict(
    )


    def run( self ):
        full_story_sentinel = ElementTree.Element(
            'div',
            name='restblogfullstory',
            id='restblogfullstory',
            style='display: none',
        )
        # For some strange reason, the preview command is causing the
        # browser to hide not only the <div id="restblogfullstory" ... />
        # tag, but the rest of the post. However, if the element has a
        # single text space to force this form <div> </div> then everything
        # works... odd, but let's work around it in any event.
        full_story_sentinel.text = ' '
        contents = ElementTree.tostring( full_story_sentinel )
        return [ nodes.raw( '', contents, format='html' ) ]


directives.register_directive( 'fullstory', FullStory )


