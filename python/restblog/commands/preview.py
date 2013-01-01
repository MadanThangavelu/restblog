# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/commands/preview.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.24 lartola    Initial working version
#


'''
Implements the ``restblog preview`` command.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


__all__ = [ 'run' ]


from optparse import OptionParser
import os
import subprocess
import tempfile

from restblog import restblog2html


USAGE = '''
restblog preview [options] <file_name> [output_file_name]

Formats a post and opens it for preview in the default web browser.

Arguments:
  file_name         A reStructuredText file.
  output_file_name  An optional file name to store the output.
                    Opens the result in a web browser by default.
'''


def run( arguments ):
    usage = USAGE.strip()
    parser = OptionParser( usage=usage )
    options = dict(
        display=True,
    )
    parser.set_defaults( **options )
    parser.add_option( '-n', '--no-display', dest='display', action='store_false', help='Does not open the file, just creates it.' )
    options, arguments = parser.parse_args( arguments )
    if not arguments:
        raise RuntimeError, 'Required arguments are missing.'
    count = len( arguments )
    if count > 3:
        raise RuntimeError, 'Unexpected arguments: %s' % ' '.join( arguments )
    file_name = arguments[0]
    output_file_name = arguments[1] if count == 2 else ''
    preview( file_name, output_file_name, display=options.display )


def preview( file_name, output_file_name='', display=True ):
    temporary_file = False
    if not output_file_name:
        temporary_file = True
        output_file, output_file_name = tempfile.mkstemp( prefix='restblog_', suffix='.html' )
        os.close( output_file )
    arguments = [ file_name, output_file_name ]
    try:
        restblog2html.main( arguments )
        if display:
            subprocess.Popen( [ 'open', output_file_name ] )
        else:
            if temporary_file:
                print 'Created %(output_file_name)s' % locals()
    except Exception, ex:
        print 'Unable to convert input file %(file_name)s into a restblog post. Error: %(ex)s' % locals()
        os.remove( output_file_name )


