# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re


class SequenceDiagramBlockPreprocessor(Preprocessor):

    RE = re.compile(r'\|{3,}\s*?\n(?P<content>[\s\S\n]*?)!(\[.*\])?\((?P<url>\S*)\)\n\|{3,}', re.MULTILINE)

    def __init__(self, media_path=None, **kwargs):
        self.media_path = media_path
        super(SequenceDiagramBlockPreprocessor, self).__init__(**kwargs)

    def run(self, lines):
        text = "\n".join(lines)

        while 1:
            m = self.RE.search(text)
            if m:
                content = m.group('content')
                image_url = m.group('url')

                if image_url.startswith('.'):
                    image_url = image_url[2:]  # ./assets/image.png -> assets/image.png

                if self.media_path is not None and not image_url.lower().startswith('http'):
                    image_url = self.media_path + image_url

                start_tag = self.markdown.htmlStash.store('<div class="visual-link-wrapper"><a href="#" data-src="%s" class="visual-link"><div class="visual-link__body"><div class="t-h6 visual-link__title">Sequence Diagram</div><p class="t-default">' % (image_url), safe=True)
                end_tag = self.markdown.htmlStash.store('</p></div><div class="visual-link__link fx-wrapper fx-s-between fx-a-center"><span class="fc-theme">View Diagram</span><span class="icon">{% svg "standard/icon-visual" %}</span></div></a></div>', safe=True)
                print_html = """<img class="visual-print-image" src="{}">""".format(image_url)

                text = '%s\n%s\n\n%s\n%s\n%s\n%s' % (text[:m.start()], start_tag, content, end_tag, print_html, text[m.end():])
            else:
                break

        return text.split("\n")


class SequenceDiagramExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'media_path': ['.', 'Path to the media'],
        }
        super(SequenceDiagramExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add SequenceDiagramBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        media_path = self.getConfig('media_path')
        md.preprocessors.add('sequence',
                             SequenceDiagramBlockPreprocessor(media_path=media_path, markdown_instance=md),
                             ">normalize_whitespace")


def makeExtension(*args, **kwargs):
    return SequenceDiagramExtension(*args, **kwargs)
