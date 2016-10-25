# -*- coding: utf-8 -*-

"""
test_links_extension
----------------------------------

Tests for `docdown.links` module.
"""

from __future__ import absolute_import, unicode_literals, print_function

import markdown
import unittest

import os


class LinksExtensionTest(unittest.TestCase):
    """
    Test the LinksExtension.
    """
    MARKDOWN_EXTENSIONS = ['docdown.links']

    EXTENSION_CONFIGS = {
        'docdown.links': {
            'link_map': {'to/nowhere': 'home/localhost'}
        }
    }

    def test_link_not_in_link_map(self):
        text = '[this is a link](http://example.com)'

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        expected_output = ('<p><a href="http://example.com">this is a link</a></p>')
        self.assertEqual(html, expected_output)

    def test_link_in_link_map(self):
        text = '[this is a link](to/nowhere)'

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        expected_output = ('<p><a href="home/localhost">this is a link</a></p>')
        self.assertEqual(html, expected_output)

    def test_link_in_link_map_with_fragment(self):
        text = '[this is a link](to/nowhere#fragment)'

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        expected_output = ('<p><a href="home/localhost#fragment">this is a link</a></p>')
        self.assertEqual(html, expected_output)
