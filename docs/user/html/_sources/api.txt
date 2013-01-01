Python API
==========

This document presents the *public* API, meaning, the set of functions and
classes that matter the most. If you are interested in all the nitty-gritty
details, here's a link to the epydoc documentation for the entire source
code: `restblog source code <../../api/index.html>`_

restblog.server
---------------

.. automodule:: restblog.server
.. autofunction:: restblog.server.connect
.. autoclass:: restblog.server.Server
.. automethod:: restblog.server.Server.getRecentPostTitles
.. automethod:: restblog.server.Server.newPost
.. automethod:: restblog.server.Server.editPost
.. automethod:: restblog.server.Server.deletePost
.. automethod:: restblog.server.Server.newPage
.. automethod:: restblog.server.Server.editPage

.. todo:: restblog.server.Server.deletePage

restblog.post
-------------

.. automodule:: restblog.post
.. autofunction:: restblog.post.createFormattedPost
.. autofunction:: restblog.post.getPostContents

restblog.directives
-------------------

.. automodule:: restblog.directives

.. automodule:: restblog.directives.restblogheader

.. automodule:: restblog.directives.fullstory

.. automodule:: restblog.directives.video

Third-party directives
----------------------

.. automodule:: restblog.directives.rstpygments

restblog.restblog2html
----------------------

.. automodule:: restblog.restblog2html
.. autofunction:: restblog.restblog2html.main

restblog.commandline
--------------------

.. automodule:: restblog.commandline
.. autofunction:: restblog.commandline.run
.. autofunction:: restblog.commandline.loadCommandByName

