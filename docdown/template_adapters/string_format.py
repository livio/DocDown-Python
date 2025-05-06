"""
Adapter to use Python str.format() to render a template
"""

from string import Formatter


class DefaultValueFormatter(Formatter):
    """
    String formatter which replaces keys found in the string but not in the replacement parameters
    with a default value.

    The default value for the default is the empty string `''`
    """

    def __init__(self, default=""):
        Formatter.__init__(self)
        self.default = default

    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                return self.default
        Formatter.get_value(key, args, kwds)


class StringFormatAdapter:
    """
    Adapter for NoteBlockPreprocessor to render templates using standard python string substitution
    using named arguments.
    """

    def render(self, template="", context=None, *args, **kwargs):
        if context is None:
            context = {}
        formatter = DefaultValueFormatter()
        return formatter.format(template, **context)
