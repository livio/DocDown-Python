# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import markdown
import unittest

from docdown.media import MediaTreeprocessor

class MediaExtensionTest(unittest.TestCase):

    EXTENSION_CONFIGS = {
        'docdown.media': {
            'media_path': 'http://example.com',
        }
    }

    MARKDOWN_EXTENSIONS = ['docdown.media']

    def test_image_tag_set_with_absolute_path_and_media_path(self):
        text = '![Alt text](/path/to/img.jpg)'
        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )
        expected_output = '<p><img alt="Alt text" src="http://example.com/path/to/img.jpg"></p>'
        self.assertEqual(html, expected_output)

    def test_image_tag_set_with_absolute_path_and_default_media_path(self):
        text = '![Alt text](/path/to/img.jpg)'
        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            #extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )
        # media_path on MediaExtension defaults to '.'
        expected_output = '<p><img alt="Alt text" src="./path/to/img.jpg"></p>'
        self.assertEqual(html, expected_output)

    def test_image_tag_set_with_absolute_path_and_no_media_path(self):
        """
        Force media_path to `None` since it defaults to `.` to ensure literal
        absolute paths are kept
        """
        text = '![Alt text](/path/to/img.jpg)'
        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs={'docdown.media': {'media_path': None,}},
            output_format='html5'
        )
        expected_output = '<p><img alt="Alt text" src="/path/to/img.jpg"></p>'
        self.assertEqual(html, expected_output)

    def test_image_tag_set_with_full_url(self):
        text = '![Alt text](http://example.org/path/to/img.jpg)'
        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )
        expected_output = '<p><img alt="Alt text" src="http://example.org/path/to/img.jpg"></p>'
        self.assertEqual(html, expected_output)
