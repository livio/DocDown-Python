# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

from .docdown import TemplateRenderMixin

class SequenceDiagramBlockPreprocessor(TemplateRenderMixin, Preprocessor):

    RE = re.compile(r'\|{3,}\s*?\n(?P<content>[\s\S\n]*?)!(\[(?P<title>.*)\])?\((?P<url>\S*)\)\n\|{3,}', re.MULTILINE)

    def __init__(self, media_path=None, prefix='', postfix='', template_adapter='docdown.template_adapters.StringFormatAdapter', **kwargs):
        self.media_url = media_path
        self.prefix = prefix
        self.postfix = postfix
        self.template_adapter = template_adapter
        super(SequenceDiagramBlockPreprocessor, self).__init__(template_adapter=template_adapter, **kwargs)

    def run(self, lines):
        text = "\n".join(lines)
        renderer = self.get_template_adapter()

        while 1:
            m = self.RE.search(text)
            if m:
                content = m.group('content')
                image_url = m.group('url')
                title = m.group('title')

                if image_url.startswith('.'):
                    image_url = image_url[2:]  # ./assets/image.png -> assets/image.png

                if self.media_url is not None:
                    if not image_url.lower().startswith('http') and not image_url.startswith('//'):
                        image_url = self.media_url + image_url

                context = {
                    'image_url': image_url,
                    'title': title
                }

                prefix = renderer.render(template=self.prefix, context=context)
                postfix = renderer.render(template=self.postfix, context=context)

                start_tag = self.markdown.htmlStash.store(prefix, safe=True)
                end_tag = self.markdown.htmlStash.store(postfix, safe=True)

                text = '%s\n%s\n\n%s\n%s\n%s' % (text[:m.start()], start_tag, content, end_tag, text[m.end():])
            else:
                break

        return text.split("\n")


class SequenceDiagramExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'prefix': ['<div>', 'Opening tag(s) which wrap the content'],
            'postfix': ['</div>', 'Closing tag(s) which wrap the content'],
            'media_path': ['.', 'Path to the media'],
            'template_adapter': ['docdown.template_adapters.StringFormatAdapter',
                                  ('Adapter for rendering prefix and postfix templates'
                                   ' using your template language of choice.')],
        }
        super(SequenceDiagramExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add SequenceDiagramBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        media_path = self.getConfig('media_path')
        prefix = self.getConfig('prefix')
        postfix = self.getConfig('postfix')
        tags = self.getConfig('tags')
        template_adapter = self.getConfig('template_adapter')

        md.preprocessors.add('sequence',
                             SequenceDiagramBlockPreprocessor(media_path=media_path,
                                                              prefix=prefix,
                                                              postfix=postfix,
                                                              template_adapter=template_adapter,
                                                              markdown_instance=md),
                             ">normalize_whitespace")


def makeExtension(*args, **kwargs):
    return SequenceDiagramExtension(*args, **kwargs)
