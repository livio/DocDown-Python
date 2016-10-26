# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class MediaTreeprocessor(Treeprocessor):

    def __init__(self, media_path=None, **kwargs):
        self.media_path = media_path
        super(MediaTreeprocessor, self).__init__(**kwargs)

    def run(self, root):
        image_tags = root.findall('.//img')
        if self.media_path is not None:
            for image_tag in image_tags:
                tag_src = image_tag.get('src').lower()
                if not tag_src.startswith('http') and not tag_src.startswith('//'):
                    # TODO: relative image tag source starting with . like sequence
                    # diagrams?

                    # Make sure we don't create a url like http://example.org//something.html
                    # if media_path ends with / and tag_src starts with /
                    # example.com/ + /blah.html = example.com/blah.html
                    # example.com + /blah.html = example.com/blah.html
                    # example.com/ + blah.html = example.com/blah.html
                    # example.com + blah.html = example.com/blah.html
                    image_tag.set('src', self.media_path.rstrip('/') + '/' + image_tag.get('src').lstrip('/'))


class MediaExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'media_path': ['.', 'Path to the media'],
        }
        super(MediaExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add MediaTreeprocessor to the Markdown instance. """
        md.registerExtension(self)

        media_path = self.getConfig('media_path')
        md.treeprocessors.add('media', MediaTreeprocessor(media_path=media_path, markdown_instance=md), '>inline')


def makeExtension(*args, **kwargs):
    return MediaExtension(*args, **kwargs)
