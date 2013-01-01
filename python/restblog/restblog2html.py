#!/usr/bin/env python

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/restblog2html.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.27 lartola    Initial working version
#


'''
Utility module that converts a reStructuredText file into XHTML.
Based on the rst2html script provided by docutils with some hard-coded
options that are suitable for restblog.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import os
import sys

from docutils.core import default_description
from docutils.core import publish_cmdline

from restblog.directives import fullstory
from restblog.directives import restblogheader
from restblog.directives import rstpygments
from restblog.directives import video


def main( arguments ):
    '''main( arguments )

    Converts a reStructuredText file into an XHTML document.

    Parameters:

    - arguments: A list of strings representing the command-line arguments
      to the ``rst2html`` executable, e.g. ``sys.argv[1:]``
    '''

    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass

    description = \
        'Generates (X)HTML documents from standalone reStructuredText ' \
        'sources ready to be posted in a restblog site. ' \
        'Highlights source code using Pygments. ' \
        + default_description

    docutils_arguments = arguments + [
        '--link-stylesheet',
        '--stylesheet=tango.css',
        '--cloak-email-addresses',
    ]

    if not arguments:
        print 'Type reStructuredText and press Control-D when done:'
    else:
        # TODO: There's gotta be a better way of communicating the source
        # file to the ``restblog.directives`` classes. For now, let's just
        # use a plain-old environment variable.
        os.environ[ 'RESTBLOG_SOURCE_FILE_NAME' ] = arguments[0]

    # Let docutils work its magic.
    publish_cmdline( writer_name='html', description=description, argv=docutils_arguments )


if __name__ == '__main__':
    main( sys.argv[1:] )


