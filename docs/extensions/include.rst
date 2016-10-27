##################
Include Extension
##################

The include DocDown tag allows for including code samples as well as CSV files into the markdown from separate files
to allow for easier maintaining and multiple inclusions. CSV files are rendered as HTML tables, otherwise files are displayed as code blocks.

The ``docdown.include`` extension requires `markdown.extensions.fenced_code`_ to be used as well.

=======
Usage
=======
In documents
-------------

.. code-block:: html

    +++ test.cpp

Python
--------------

.. code-block:: python

   _root = os.path.dirname(os.path.abspath(__file__))
    asset_dir = os.path.join(_root, 'test_files', 'assets')

    config = {
        'docdown.include': {
            'asset_directory': asset_dir,
            'root_directory': asset_dir,
            'extension_map': {
                '.m': '.c',
            }
        }
    }

    text = '+++ test.json'

    html = markdown.markdown(
            text,
            extensions= [
                'markdown.extensions.fenced_code',
                'docdown.include'],
            extension_configs=config,
            output_format='html5')

=======
Output
=======

Where test.json contains

.. code-block:: json

  {
     "test": "json",
     "asdf": true
   }

HTML output will be

.. code-block:: html

    <p>Test JSON:</p>
     <pre><code class="json">
       &quot;test&quot;:
       &quot;content&quot;}
     </code></pre>


.. _`markdown.extensions.fenced_code`: https://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html
