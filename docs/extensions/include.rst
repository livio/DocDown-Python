##################
Includes
##################

The include DocDown tag allows for including code samples as well as CSV files into the markdown from separate files
to allow for easier maintaining and multiple inclusions. CSV files are rendered as HTML tables, otherwise files are displayed as code blocks.

Files will be looked for initially under ``current_directory/asset_directory/``.  If not found, one directory will
be removed from ``current_directory`` until ``current_directory`` is the same as ``root_directory``.

=============
Dependencies
=============
The ``docdown.include`` extension requires `markdown.extensions.fenced_code`_ to be used as well.

==============
Configuration
==============

root_directory
    Base directory where source code files to include can be found.  The extension will not look above this
    directory for source code includes.
current_directory
    The lowest level nested directory to start searching for source code includes in.  The extension will start
    here and roll up until ``root_directory``
asset_directory
    A directory within ``current_directory`` where the source code includes exist.

----------
Example
----------
* /mnt/media/
  * assets/
  * c/assets/
  * c/headers/assets/


A configuration where ``root_directory`` is ``/mnt/media/``, ``current_directory`` is ``/mnt/media/c/headers/``,
and ``asset_directory`` is ``assets`` would start looking for a file in ``/mnt/media/c/headres/assets/``.  If it is
not found then the next directory checked would be ``/mnt/media/c/assets/``, and then ``/mnt/media/assets/``

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
    root_directory = os.path.join('/', 'projects', 'src')
    current_directory = os.path.join(_root, 'test_files', 'nested', 'path')

    config = {
        'docdown.include': {
            'asset_directory': asset_dir,
            'root_directory': current_directory,
            'current_directory':
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
