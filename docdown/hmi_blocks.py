# -*- coding: utf-8 -*-

"""
hmi_blocks
----------------------------------

docdown.hmi_blocks Markdown extension module
"""

from __future__ import absolute_import, unicode_literals, print_function

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re


class HmiListBlockPreprocessor(Preprocessor):

    RE = re.compile(r'''
(?P<fence>^(?:!{3,}))\W(?P<type>\w+)\W*\n
(?P<content>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)

    SVG_MAP = {
        'must': 'standard/icon-must',
        'note': 'standard/icon-note',
        'may': 'standard/icon-may',
        'sdl': 'standard/icon-sdl',
    }

    TITLE_MAP = {
        'must': 'Must',
        'note': 'Note',
        'may': 'May',
        'sdl': 'SDL',
    }

    def run(self, lines):
        text = "\n".join(lines)

        while 1:
            m = self.RE.search(text)
            if m:
                fence_type = m.group('type')
                css_class = fence_type.lower()
                content = m.group('content')
                svg = self.SVG_MAP.get(css_class, self.SVG_MAP.get('note'))
                svg_path = "svg/{}.svg".format(svg)
                title = self.TITLE_MAP.get(css_class, css_class.capitalize())

                if css_class not in self.SVG_MAP.keys():
                    css_class = 'note'

                prefix = '<div class="{}"><div class="icon">{{% svg "{}" %}}<img class="icon--pdf" src="{{% static "{}" %}}"></div><h5>{}</h5>'.format(css_class, svg, svg_path, title)

                start_tag = self.markdown.htmlStash.store(prefix, safe=True)
                end_tag = self.markdown.htmlStash.store('</div>', safe=True)

                text = '%s\n%s\n\n%s\n%s\n%s' % (text[:m.start()], start_tag, content, end_tag, text[m.end():])
            else:
                break

        return text.split("\n")


class HmiListExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add HmiListBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('hmi_list',
                             HmiListBlockPreprocessor(md),
                             ">normalize_whitespace")


def makeExtension(*args, **kwargs):
    return HmiListExtension(*args, **kwargs)
