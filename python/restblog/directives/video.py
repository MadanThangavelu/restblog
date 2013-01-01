# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/directives/video.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.07.30 lartola    Initial working version
#

'''
The restblog video directive.

Usage::

    .. video:: url

Or::

    .. video:: type id

Options::

    :width: 400
    :height: 300
    :fullscreen: yes
    :scriptaccess: yes

Options for vimeo only::

    :title: yes
    :byline: yes
    :portrait: yes

Examples::

    .. video:: http://vimeo.com/7809605
    .. video:: vimeo 7809605
    .. video:: http://www.youtube.com/watch?v=37GrbCUvZEM
    .. video:: youtube 37GrbCUvZEM

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''

import os
import re

from docutils import nodes
from docutils.parsers.rst import directives 
from docutils.parsers.rst import Directive


class Video( Directive ):

    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True

    def yesOrNo( value ):
        return directives.choice( value, ( 'yes', 'no', ) )

    option_spec = dict(
        width=directives.positive_int,
        height=directives.positive_int,
        title=yesOrNo,
        byline=yesOrNo,
        portrait=yesOrNo,
        fullscreen=yesOrNo,
        scriptaccess=yesOrNo,
    )


    def run( self ):

        service = None
        if len( self.arguments ) == 2:
            service, id = self.arguments
        else:
            url = self.arguments[0]
            vimeo = re.compile( '^(https?://)?[^/]*vimeo\.[^/]*/(\d+)$' )
            youtube = re.compile( '^(https?://)?[^/]*youtube\.[^/]*/watch\?v=([^&]*)' )
            match = vimeo.match( url )
            if match:
                service = 'vimeo'
                id = match.group(2)
            elif not match:
                match = youtube.match( url )
                if match:
                    service = 'youtube'
                    id = match.group(2)
        if service not in ( 'vimeo', 'youtube', ):
            raise ValueError, 'Do not know how to handle video of type %(service)s' % locals()

        values = dict(
            id=id,
            width=self.options.get( 'width', 400 ),
            height=self.options.get( 'height', 300 ),
            title=(1 if self.options.get( 'title', 'yes' ) else 0),
            byline=(1 if self.options.get( 'byline', 'yes' ) else 0),
            portrait=(1 if self.options.get( 'portrait', 'yes' ) else 0),
            fullscreen=(1 if self.options.get( 'fullscreen', 'yes' ) else 0),
            fullsreen_string=('true' if self.options.get( 'fullscreen', 'yes' ) else 'false'),
            scriptaccess=('always' if self.options.get( 'scriptaccess', 'yes' ) else 'never'),
        )

        templates = dict(
            vimeo='''
<object width="%(width)s" height="%(height)s">
    <param name="allowfullscreen" value="%(fullsreen_string)s" />
    <param name="allowscriptaccess" value="%(scriptaccess)s" />
    <param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%(id)s&amp;server=vimeo.com&amp;show_title=%(title)s&amp;show_byline=%(byline)s&amp;show_portrait=%(portrait)s&amp;color=&amp;fullscreen=%(fullscreen)s" />
    <embed src="http://vimeo.com/moogaloop.swf?clip_id=%(id)s&amp;server=vimeo.com&amp;show_title=%(title)s&amp;show_byline=%(byline)s&amp;show_portrait=%(portrait)s&amp;color=&amp;fullscreen=%(fullscreen)s" type="application/x-shockwave-flash" allowfullscreen="%(fullsreen_string)s" allowscriptaccess="%(scriptaccess)s" width="%(width)s" height="%(height)s">
    </embed>
</object>
            ''',
            youtube='''
<object width="%(width)s" height="%(height)s">
    <param name="allowfullscreen" value="%(fullsreen_string)s" />
    <param name="allowscriptaccess" value="%(scriptaccess)s" />
    <param name="movie" value="http://www.youtube.com/v/%(id)s&amp;hl=en_US&amp;fs=%(fullscreen)s"></param>
    <embed src="http://www.youtube.com/v/%(id)s&amp;hl=en_US&amp;fs=%(fullscreen)s" type="application/x-shockwave-flash" allowscriptaccess="%(scriptaccess)s" allowfullscreen="%(fullsreen_string)s" width="%(width)s" height="%(height)s"></embed>
</object>
            ''',
        )

        contents = templates[ service ] % values

        return [ nodes.raw( '', contents, format='html' ) ]


directives.register_directive( 'video', Video )


