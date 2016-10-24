# -*- coding: utf-8 -*-

"""
Adapter to use Python str.format() to render a template
"""

from __future__ import absolute_import, unicode_literals, print_function


class StringFormatAdapter(object):
    """
    Adapter for NoteBlockPreprocessor to render templates using standard python string substitution
    using named arguments.
    """
    def render(self, template='', context=None, *args, **kwargs):
        if context is None:
            context = {}
        return template.format(template, **context)
