restblog directives for docutils
================================

Besides all the standard directives provided by docutils the following are
specific for blogging with restblog.

``.. restblog::``
-----------------

This is the main directive that identifies and describes either a post or a
page.

Options:

- ``:categories:``

    :Type: string
    :Default: empty

    Comma-separated list of strings with the names of the categories.
    Categories must exist in the Wordpress blog already.

- ``:id:``

    :Type: integer
    :Default: empty

    Post ID. This gets automatically filled-in by ``restblog`` immediately
    after inserting a post from a ``.rst`` text file.

- ``:publish:``

    :Type: string
    :Valid values: yes or no
    :Default: yes

    Whether the post or page should be immediately available in the blog upon
    insertion or not.

- ``:source:``

    :Type: string
    :Valid values: yes or no
    :Default: no

    When set to ``yes``, ``restblog`` would include the actual
    reStructuredText source that produced the HTML contents. This is similar
    to what ``Sphinx`` would do.

    **Important** This feature is currently disabled by default because the
    code is put into an invisible ``<div/>`` in the HTML at the beginning of
    the post body. This turned out to be problematic because Wordpress and
    other related tools, e.g. RSS feeds, ignore all attributes in the XML tags
    causing the source code to show up first in the RSS. This is very
    distracting and not ideal. Need to create a ``docutils`` ``transform`` to
    place the code at the end of the contents. This is in the list of things
    to do.

- ``:tags:``

    :Type: string
    :Default: empty

    Comma-separated list of strings with the names of the tags.
    Tags need not exist already and can be pretty much anything you like.

- ``:title:``

    :Type: string
    :Default: empty

    The title for the post or page. If left empty, ``restblog`` would use the
    name of the source file as the title.

- ``:type:``

    :Type: string
    :Valid values: post or page
    :Default: post

    Whether this is a post or a page.


``.. fullstory::``
------------------

Separates the excerpt from the rest of the contents. This basically translates
into the ``<!--more-->`` tag that Wordpress uses to determine the excerpt.

``.. video::``
--------------

Embeds a video from either vimeo or YouTube. It can be used in two ways:

#. URL::

    .. video:: url

   Examples::

    .. video:: http://vimeo.com/7809605

    .. video:: http://www.youtube.com/watch?v=qVDUYJo3CjU

#. Service and video ID::

    .. video:: service video

   Examples::

    .. video:: vimeo 7809605

    .. video:: youtube qVDUYJo3CjU

Options:

- ``:width:``

    :Type: integer
    :Default: 400

- ``:height:``

    :Type: integer
    :Default: 300

- ``:fullscreen:``
    
    :Type: string
    :Valid values: yes or no
    :Default: yes

- ``:scriptaccess:``

    :Type: string
    :Valid values: yes or no
    :Default: yes

Options for vimeo only:

- ``:title:``

    :Type: string
    :Valid values: yes or no
    :Default: yes

- ``:byline:``

    :Type: string
    :Valid values: yes or no
    :Default: yes

- ``:portrait:``

    :Type: string
    :Valid values: yes or no
    :Default: yes

``.. sourcecode::``
-------------------

This is a verbatim copy of the Pygments directive that provides beautiful
syntax highlighting for a wide range of programming and scripting languages.
It is copyrighted by the Pygments authors:

:copyright: Copyright 2006-2009 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.

Verbatim documentation from original authors:

.. automodule:: restblog.directives.rstpygments


