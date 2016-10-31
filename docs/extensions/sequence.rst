##################
Sequence Diagrams
##################

Sequence diagrams allow for including diagram images that can be opened to be be separately vs be included directly in
the HTML as a standard image.

A sequence diagram is bracketed by three pipes ||| and the last line of the block should be a markdown image tag.
The alt title of this image can be left blank to default to Sequence Diagram, otherwise this will be used as the title
for the sequence diagram block.

The configuration for the sequence diagrams has a prefix and postfix template strings which can be templated using
any of the provided :doc:`../template_adapters/index` template renderers or with a custom renderer.  The default renderer
uses standard Python ``str.format()`` substitutions for templating.

The context will include image_url and title which come from the markdown image tag. The markdown image tag is not rendered,
only the content within the tag. The image url is also updated to include the media url from the configuration.

=========
Usage
=========

HTML
--------

.. code-block:: html

   |||
   Activate App
   ![Activate App Sequence Diagram](./assets/ActivateApp.png)
   |||


Python
---------

.. code-block:: python

    config = {
        'docdown.sequence': {
            'media_url': 'https://example.com/media/',
            'prefix': ('<div class="visual-link-wrapper">\n'
                       '<a href="#" data-src="{{{ image_url }}}" class="visual-link">\n'
                       '<div class="visual-link__body">\n<div class="t-h6 visual-link__title">{{ title }}</div>\n'
                       '<p class="t-default">\n'),
            'postfix': ('</p></div><div class="visual-link__link fx-wrapper fx-s-between fx-a-center">\n'
                        '<span class="fc-theme">View Diagram</span>\n'
                        '<span class="icon">{% svg "standard/icon-visual" %}</span>\n'
                        '</div>\n</a>\n</div>\n<img class="visual-print-image" src="{{{ image_url }}}">'),
        }
    }

    text = ('# Sequence Diagrams\n'
            '|||\n'
            'Activate App\n'
            '![Activate App Sequence Diagram](./assets/ActivateApp.png)\n'
            '|||')

    html = markdown.markdown(
        text,
        extensions=['docdown.sequence'],
        extension_configs=config,
        output_format='html5')


=======
Output
=======

.. code-block:: html

    <div class="visual-link-wrapper">
      <a href="#" data-src="https://example.com/media/assets/ActivateApp.png" class="visual-link">
        <div class="visual-link__body">
            <div class="t-h6 visual-link__title">Activate App Sequence Diagram</div>
            <p class="t-default">
                <p>Activate App</p>
            </p>
        </div>
        <div class="visual-link__link fx-wrapper fx-s-between fx-a-center">
            <span class="fc-theme">View Diagram</span>
            <span class="icon">{% svg "standard/icon-visual" %}</span>
        </div>
      </a>
    </div>
    <img class="visual-print-image" src="https://smartdevicelink.com/media/assets/ActivateApp.png">
