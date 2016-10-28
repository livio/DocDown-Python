################
Media
################

The media DocDown extension updates all images that do not start with http or // to use the configurable media URL.

======
Usage
======

HTML
-----

.. code-block:: html

   ![Alt Text](http://example.com/static/img/image.png)
   ![Alt Text](assets/image.png)
   ![Alt Text](./assets/image.png)


Python
-------
.. code-block:: python

    config = {
        'docdown.media': {
            'media_url': 'https://example.com/media/'
        }
    }

    text = ('![Alt Text](/path/to/image.png)\n'
            '![Alt Text](assets/image.png)\n'
            '![Alt Text(./assets/image.png)\n')
    html = markdown.markdown(
        text,
        extensions=['docdown.media'],
        extension_configs=config,
        output_format='html5'
    )

========
Output
========

.. code-block:: html

   <p><img src="http://example.com/static/img/image.png" alt="Alt Text"></p>
   <p><img src="https://example.com/media/assets/image.png" alt="Alt Text"></p>
   <p><img src="https://example.com/media/assets/image.png" alt="Alt Text"></p>
