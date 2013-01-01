restblog in 5 minutes
=====================

This gives you a tour of all you can do with restblog.

What you need
-------------

All you need is a text editor and a shell, terminal or command prompt.
You also need to have a Wordpress blog already installed with XMLRPC enabled.

Connecting to your blog
-----------------------

Type the following on a shell::

    restblog init your.blog.com http://your.blog.com/xmlrpc.php user --interactive

Type your password at the prompt.

This creates a directory called ``your.blog.com`` under your current directory
and connects to the given URL with the given user name. The ``--interactive``
flag prompts for a password so you don't have to type it in the command-line
directly.

Now, let's make that your current directory::

    cd your.blog.com

Listing recent posts
--------------------

The following command lists the most recent posts in your blog::

    restblog list

For example::

    2   Second post         20100707 07:07
    1   Hello world!        20100701 01:00

Drafting a post
---------------

::

    restblog draft new-post.rst --title='New post using restblog!'

This creates a file named ``new-post.rst`` that looks like this::

    .. restblog::
        :title: New post using restblog!
        :type: post

    .. Replace this line with the contents of your post

Simply open this file with a text editor of your choice and write the contents
of your post, e.g.::

    .. restblog::
        :title: New post using restblog!
        :type: post

    This is an example of creating a post using ``restblog``.

    .. fullstory::

    It also supports explicit excerpts. By using the ``.. fullstory::``
    directive directly above from this line, it splits the post into excerpt
    and full contents.

Save it and go back to your shell.

Inserting the post
------------------

::

    restblog insert new-post.rst

That's it! Go to a web browser and you will see your new post published.

After inserting a post, ``restblog`` puts more metdata into the ``..
restblog::`` directive used in the post. The directive for the post above
would look like this after the insertion::

    .. restblog::
        :categories: 
        :id: 3
        :publish: yes
        :source: no
        :tags:
        :title: New post using restblog!
        :type: post

The directive is explained in full detailed in this page
:ref:`directives-restblog`.

Classifying and tagging a post
------------------------------

The ``.. restblog::`` directive supports two options: ``:categories`` and
``:tags:``. Both expect a comma-separated list of strings. Let's classify the
post inserted above. Open ``new-post.rst`` again in a text editor and change
the contents of these two options to look like this::

    :categories: Uncategorized
    :tags: demo, restblog

Updating a post
---------------

After you modify the contents of a previosly inserted post, you can send the
changes to your blog by typing the following::

    restblog update new-post.rst

In the example above, the post would now appear under the *Uncategorized*
category and will be tagged as *demo* and *restblog*. 

Deleting a post
---------------

All you need is the post ID and the ``delete`` command, e.g.::

    restblog delete 3

Would delete the post inserted above.

Managing pages
--------------

Inserting, updating and deleting pages works exactly the same as with posts.
The only two things to distinguish them are:

#. The ``:type:`` option for the ``.. restblog::`` directive should be set to
   ``page`` instead of ``post``, e.g.::

    .. restblog::
        :title: Examples
        :type: page

#. The ``draft`` command provides a ``--page`` option, e.g.::

    restblog draft new-page.rst --title='Examples' --page

That's pretty much it.

The following sections describe the directives that can be used in your posts.
Also, documentation about the internals of restblog and API for developers.

