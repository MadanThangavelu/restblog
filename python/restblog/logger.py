# No shebang line. This module is meant to be imported.

#
# Copyright 2010. Luis Artola. All rights reserved.
#

#
# $URL: file:///svn/restblog/trunk/src/python/restblog/logger.py $
# $Date: 2010-07-31 14:27:54 -0700 (Sat, 31 Jul 2010) $
# $Revision: 186 $
#
# History:
# 2010.06.29 lartola    Initial working version
#


'''
Basic logging services.

:copyright: Copyright 2010 Luis Artola.
:license: BSD, see LICENSE.txt for details.
'''


import logging


logger = logging.getLogger( 'restblog.console' )

formatter = logging.Formatter( '%(levelname)-8s | %(message)s', '%Y%m%d.%H%M' )
handler = logging.StreamHandler()
handler.setFormatter( formatter )
logger.addHandler( handler )
logger.setLevel( logging.INFO )


