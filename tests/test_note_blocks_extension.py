# -*- coding: utf-8 -*-

"""
test_note_blocks_extension
----------------------------------

Tests for `docdown.note_blocks` module.
"""

from __future__ import absolute_import, unicode_literals, print_function

import copy
import markdown
import unittest

class NoteBlockExtensionTest(unittest.TestCase):
    """
    Integration test with markdown for :class:`docdown.note_blocks.NoteBlockExtension`
    """
    MARKDOWN_EXTENSIONS = ['docdown.note_blocks']
    EXTENSION_CONFIGS = {
        'docdown.note_blocks': {
            'prefix': ('<div class="{tag}"><div class="icon">{{% svg "{svg}" %}}'
                       '<img class="icon--pdf" src="{{% static "{svg_path}" %}}"></div><h5>{title}</h5>'),
            'postfix': '</div>',
            'tags': {
                'must': {
                    'svg': 'standard/icon-must',
                    'svg_path': 'svg/standard/icon-must.svg',
                    'title': 'Must'
                },
            },
        }
    }

    def test_render_stringformatadapter_with_prefix_and_postfix(self):
        text = ('!!! MUST\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extension_configs=self.EXTENSION_CONFIGS,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = (
            '<div class="must"><div class="icon">'
            '{% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}">'
            '</div><h5>Must</h5>\n\n<p>hello world</p>\n</div>')
        self.assertEqual(html, expected_output)

    def test_render_stringformatadapter_default_pre_and_postfix(self):
        text = ('!!! MUST\n'
                'hello world\n'
                '!!!')

        config = copy.deepcopy(self.EXTENSION_CONFIGS)
        del(config['docdown.note_blocks']['prefix'])
        del(config['docdown.note_blocks']['postfix'])

        html = markdown.markdown(
            text,
            extension_configs=config,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = '<div>\n\n<p>hello world</p>\n</div>'
        self.assertEqual(html, expected_output)

    def test_render_templatestringadapter_with_prefix_and_postfix(self):
        config = {
            'docdown.note_blocks': {
                'template_adapter': 'docdown.template_adapters.TemplateStringAdapter',
                'prefix': ('<div class="$tag"><div class="icon">{% svg "$svg" %}'
                           '<img class="icon--pdf" src="{% static "$svg_path" %}"></div><h5>$title</h5>'),
                'postfix': '</div>',
                'tags': {
                    'must': {
                        'svg': 'standard/icon-must',
                        'svg_path': 'svg/standard/icon-must.svg',
                        'title': 'Must'
                    },
                },
            }
        }

        text = ('!!! MUST\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extension_configs=config,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = (
            '<div class="must"><div class="icon">'
            '{% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}">'
            '</div><h5>Must</h5>\n\n<p>hello world</p>\n</div>')
        self.assertEqual(html, expected_output)

    def test_render_pystacheadapter_with_prefix_and_postfix(self):
        config = {
            'docdown.note_blocks': {
                'template_adapter': 'docdown.template_adapters.PystacheAdapter',
                'prefix': ('<div class="{{ tag }}"><div class="icon">{% svg "{{ svg }}" %}'
                           '<img class="icon--pdf" src="{% static "{{ svg_path }}" %}"></div><h5>{{ title }}</h5>'),
                'postfix': '</div>',
                'tags': {
                    'must': {
                        'svg': 'standard/icon-must',
                        'svg_path': 'svg/standard/icon-must.svg',
                        'title': 'Must'
                    },
                },
            }
        }

        text = ('!!! MUST\n'
                'hello world\n'
                '!!!')

        html = markdown.markdown(
            text,
            extension_configs=config,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = (
            '<div class="must"><div class="icon">'
            '{% svg "standard/icon-must" %}<img class="icon--pdf" src="{% static "svg/standard/icon-must.svg" %}">'
            '</div><h5>Must</h5>\n\n<p>hello world</p>\n</div>')
        self.assertEqual(html, expected_output)
