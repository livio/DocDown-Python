###################
Template Adapters
###################

Some DocDown extensions make use of blocks of HTML which the user may configure via templates.  Python DocDown
uses template adapter classes which provide a ``render(template, context)`` method to allow for a configurable
templating language to be used.  The templatable extensions have a `template_adapter` configuration paramters which
takes the module and class to use, such as ``docdown.template_adapters.StringFormatAdapter``.

The following template adapters are provided by the Python DocDown package.

* ``docdown.template_adapters.StringFormatAdapters``
    This is the default adapter.  It uses standard Python `string formatting`_ for the templates.
* ``docdown.template_adapters.TemplateStringAdapter``
    ``TemplateStringAdapter`` uses Python `template strings`_ for the HTML template.
* ``docdown.template_adapters.PystacheAdapter``
    An adapter to use Mustache_ templates via the Pystache_ package.



.. _`string formatting`: https://docs.python.org/3.5/library/stdtypes.html#str.format
.. _`template strings`: https://docs.python.org/3.5/library/string.html#template-strings
.. _Mustache: 'https://mustache.github.io/'
.. _Pystache: 'https://pypi.python.org/pypi/pystache'
