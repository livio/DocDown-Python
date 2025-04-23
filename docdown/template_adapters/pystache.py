"""
Adapter to use pystache to render a mustache template
"""

import pystache  # type: ignore


class PystacheAdapter:
    """
    Adapter for NoteBlockPreprocessor to render mustache templates using pystache
    """

    def render(self, template="", context=None, *args, **kwargs):
        if context is None:
            context = {}

        renderer = pystache.Renderer()
        return renderer.render(template, context)
