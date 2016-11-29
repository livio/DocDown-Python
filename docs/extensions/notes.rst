######################
Note Blocks
######################

Note blocks allows for calling out content in note like fashion. The note type context is configurable through the options
passed to the markdown extension.

A note block is delimited by three exclamation points. The beginning exclamation point also includes the note type.

The configuration for the notes has a prefix and postfix template strings which can be templated using
any of the provided :doc:`../template_adapters/index` template renderers or with a custom renderer.  The default
renderer uses standard Python ``str.format()`` substitutions for templating.

==============
Configuration
==============

prefix
    String which prefix the note block text.  This can be templated using any of the provided
    :doc:`../template_adapters/index` template renderers or with a custom renderer.
postfix
    String which will be appended to the note block text.  This can be templated using any of the provided
    :doc:`../template_adapters/index` template renderers or with a custom renderer.
tags
    A dict of tag names which are also dicts of configuration.  The keys and values will be used as template
    context for the prefix and postfix templates.  The tag key will additionally be added to this with a key of
    ``tag``.
default_tag
    The name of a tag to use as the default if the markdown string specifies one which is not configured in the
    tags dict.


=======
Usage
=======
In documents
-------------

.. code-block:: html

   !!! MUST
   hello world!
   !!!

   !!! MAY
   I have a custom prefix and postfix
   !!!

   !!! DEFAULT
   I will look like MUST was specified
   !!!'

Python
--------------

.. code-block:: python

    config = {
        'docdown.note_blocks': {
            'prefix': ('<div class="{tag}">\n<div class="icon">\n{{% svg "{svg}" %}}'
                       '<img class="icon--pdf" src="{{% static "{svg_path}" %}}">\n</div>\n<h5>{title}</h5>'),
            'postfix': '</div>',
            'default_tag': 'must',
            'tags': {
                'must': {
                    'svg': 'standard/icon-must',
                    'svg_path': 'svg/standard/icon-must.svg',
                    'title': 'Must',
                },
                'may': {
                    'svg': 'standard/icon-may',
                    'svg_path': 'svg/standard/icon-may.svg',
                    'title': 'May',
                    'prefix': ('<div class="custom-prefix {tag}">\n<div class="icon">\n{{% svg "{svg}" %}}'
                               '<img class="icon--pdf" src="{{% static "{svg_path}" %}}">\n</div>\n<h5>{title}</h5>'),
                    'postfix': '<span>Custom Postfix</span></div>',
                },
            },
        },
    }

    text = ('!!! MUST\n'
            'hello world\n'
            '!!!\n\n'
            '!!! MAY\n'
            'I have a custom prefix and postfix\n'
            '!!!\n\n'
            '!!! DEFAULT\n'
            'I will look like MUST was specified\n'
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

   <div class="custom-prefix may">
   <div class="icon">
   {% svg "standard/icon-may" %}<img class="icon--pdf" src="{% static "svg/standard/icon-may.svg" %}">
   </div>
   <h5>May</h5>

   <p>I have a custom prefix and postfix</p>
   <span>Custom Postfix</span></div>

   <div class="must">
   <div class="icon">
   {% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}">
   </div>
   <h5>Must</h5>

   <p>I will look like MUST was specified</p>
   </div>
