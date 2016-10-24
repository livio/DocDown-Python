# -*- coding: utf-8 -*-

"""
test_hmi_blocks_extension
----------------------------------

Tests for `docdown.hmi_blocks` module.
"""

from __future__ import absolute_import, unicode_literals, print_function

import markdown
import unittest

class HmiListExtensionTest(unittest.TestCase):
    """
    Integration test with markdown for :class:`docdown.hmi_blocks.HmiListExtension`
    """
    MARKDOWN_EXTENSIONS = ['docdown.hmi_blocks']

    def test_generic_note(self):
        text = ('!!! MUST\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '''<div class="must"><div class="icon">{% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}"></div><h5>Must</h5>\n\n<p>hello world</p>\n</div>'''
        self.assertEqual(html, expected_output)

    def test_important_note(self):
        text = ('!!! MAY\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '''<div class="may"><div class="icon">{% svg "standard/icon-may" %}<img class="icon--pdf" src="{% static "svg/standard/icon-may.svg" %}"></div><h5>May</h5>\n\n<p>hello world</p>\n</div>'''
        self.assertEqual(html, expected_output)

    def test_sdl_related_behavior_note(self):
        text = ('!!! NOTE\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '''<div class="note"><div class="icon">{% svg "standard/icon-note" %}<img class="icon--pdf" src="{% static "svg/standard/icon-note.svg" %}"></div><h5>Note</h5>\n\n<p>hello world</p>\n</div>'''
        self.assertEqual(html, expected_output)

    def test_must_note(self):
        text = ('!!! SDL\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '''<div class="sdl"><div class="icon">{% svg "standard/icon-sdl" %}<img class="icon--pdf" src="{% static "svg/standard/icon-sdl.svg" %}"></div><h5>SDL</h5>\n\n<p>hello world</p>\n</div>'''
        self.assertEqual(html, expected_output)

    def test_block_content_list(self):
        text = ('!!! MUST\n'
                '1. list item 1\n'
                '    * sub list item 1\n'
                '    * sub list item 2\n'
                '2. list item 2\n'
                '3. list item 3\n'
                '!!!')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        expected_output = '''<div class="must"><div class="icon">{% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}"></div><h5>Must</h5>\n\n<ol>\n<li>list item 1<ul>\n<li>sub list item 1</li>\n<li>sub list item 2</li>\n</ul>\n</li>\n<li>list item 2</li>\n<li>list item 3</li>\n</ol>\n</div>'''
        self.assertEqual(html, expected_output)

    def test_random(self):
        text = ('!!! info\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '''<div class="note"><div class="icon">{% svg "standard/icon-note" %}<img class="icon--pdf" src="{% static "svg/standard/icon-note.svg" %}"></div><h5>Info</h5>\n\n<p>hello world</p>\n</div>'''
        self.assertEqual(html, expected_output)
