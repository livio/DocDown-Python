"""
Adapter to use Python string.Template to render a template
"""

from string import Template


class TemplateStringAdapter:
    def render(self, template="", context=None, *args, **kwargs):
        if context is None:
            context = {}

        t = Template(template)
        return t.substitute(**context)
