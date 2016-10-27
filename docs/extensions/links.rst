#######
Links
#######

The Links DocDown extension allow for custom, pre-generated links to be reference from normal markdown link syntax. Via the configuration, a link map can be included which provides a dictionary of names to URLs. All the links are checked against this dictionary and if found in the dictionary, the URL provided in the dictionary replaces the URL in the markdown.

=======
Usage
=======

In documents
-------------

.. code-block:: html

   [this is a link](http://mobelux.com/)
   [this is a link](to/nowhere)
   [this is a link](to/nowhere#testhash)

Python
--------------

.. code-block:: python

    config = {
        'docdown.links': {
            'link_map': {
                'to/nowhere': 'home/localhost',
            },
        }
    }

    text = ('[this is a link](http://mobelux.com/)\n'
            '[this is a link](to/nowhere)\n'
            '[this is a link](to/nowhere@testhash)')
    html = markdown.markdown(
            text,
            extensions=['docdown.links'],
            extension_configs=config,
            output_format='html5')

=======
Output
=======

.. code-block:: html

   <p><a href="http://mobelux.com/">this is a link</a></p>
   <p><a href="home/localhost">this is a link</a></p>
   <p><a href="home/localhost#testhash">this is a link</a></p>
