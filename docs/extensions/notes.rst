######################
Note Blocks Extension
######################

Note blocks allows for calling out content in note like fashion. The note type context is configurable through the options
passed to the markdown extension.

A note block is delimited by three exclamation points. The beginning exclamation point also includes the note type.

=======
Usage
=======
In documents
-------------

.. code-block:: html

  !!! MUST
   hello world!
   !!!

Python
--------------

.. code-block:: python

  config = {
      'docdown.note_blocks': {
          'prefix': ('<div class="{tag}">\n<div class="icon">\n{{% svg "{svg}" %}}'
                     '<img class="icon--pdf" src="{{% static "{svg_path}" %}}">\n</div>\n<h5>{title}</h5>'),
          'postfix': '</div>',
          'tags': {
              'must': {
                  'svg': {
                      'standard/icon-must',
                      'svg_path': 'svg/standard/icon-must.svg',
                      'title': 'Must'
                  },
              },
           },
       },
    }

    text = ('!!! MUST\n'
            'hello world\n'
            '!!!')

    html = markdown.markdown(
            text,
            extensions=['docdown.note_blocks'],
            extension_configs=config,
            output_format='html5')

=======
Output
=======

.. code-block:: html

  <div class="must">
   <div class="icon">
   {% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}">
   </div>
   <h5>Must</h5>

   <p>hello world</p>
   </div>
