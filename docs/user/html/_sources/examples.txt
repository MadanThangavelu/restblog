Examples
========

The canonical "Hello World" of restblog
---------------------------------------

::

    .. restblog::
        :title: Hello restblog world!

    This simple post was created with `restblog
    <http://luisartola.com/software/restblog>`_.

An example with source code for technical bloggers
--------------------------------------------------

::

    .. restblog::
        :title: Sample code

    This sample post was created with `restblog
    <http://luisartola.com/software/restblog>`_.

    It also uses the nifty `Pygments <http://pygments.org>`_ Python package to
    highlight syntax in source code snippets. 

    Here are some examples:

    C++
    ---

    .. sourcecode:: c++

        #include <iostream>

        int main( int argc, char* argv[] ) 
        {
            std::cout << "Hello world!" << std::endl;
            return 0;
        }


    Python
    ------

    .. sourcecode:: python

        if __name__ == '__main__':
            print 'Hello world!'

    XML
    ---

    .. sourcecode:: xml

        <values>
            <value name='one'>1</value>
            <value name='two'>2</value>
        </values>

Embedding videos
----------------

::

    .. restblog::
        :title: Embedded video!

    Support embedding video from vimeo or YouTube in two ways:

    #. Directly from a URL:

        .. video:: http://vimeo.com/7809605

        .. video:: http://www.youtube.com/watch?v=37GrbCUvZEM

    #. Or, by service and video ID:
    
        .. video:: vimeo 7809605

        .. video:: youtube 37GrbCUvZEM

Simple page
-----------

::

    .. restblog::
        :title: Thoughts
        :type: page

    Managing pages is extremely simple, just specify ``:type: page`` in the
    ``.. restblog::`` directive.


