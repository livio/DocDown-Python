# -*- coding: utf-8 -*-

"""
test_media_carousels_extension
----------------------------------

Tests for `docdown.media_carousels` module.
"""

from __future__ import absolute_import, unicode_literals, print_function

import copy
import markdown
import unittest
from docdown.media_carousels import BEFORE_CAROUSEL_HTML, AFTER_CAROUSEL_HTML


class MediaCarouselExtensionTest(unittest.TestCase):
    """
    Integration test with markdown for :class:`docdown.media_carousels.MediaCarouselExtension`
    """
    MARKDOWN_EXTENSIONS = ['docdown.media_carousels']
    CAROUSEL_OPEN_FENCE = "[carousel!]"
    CAROUSEL_CLOSE_FENCE = "[!carousel]"
    PREVIEW_CLASS = 'small-preview'

    base_image_string = "!["
    maxDiff = 1000

    def test_empty_string(self):
        text = ''

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )
        expected_output = ''
        self.assertEqual(html, expected_output)

    def test_nothing_matching(self):
        heading = 'Test'
        text = f'# {heading}'

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        expected_output = f"<h1>{heading}</h1>"
        self.assertEqual(expected_output, html)

    def test_full_match_empty(self):
        """An empty carousel with no images"""
        text = self.CAROUSEL_OPEN_FENCE + self.CAROUSEL_CLOSE_FENCE

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        expected_output = BEFORE_CAROUSEL_HTML.format(0) + AFTER_CAROUSEL_HTML
        self.assertEqual(expected_output, html)

    def test_full_match(self):
        """A carousel with an image"""
        img_alt = 'image text'
        img_title = 'image title'
        img_path = 'path/to/img.jpg'
        image_string = f'![{img_alt}]({img_path} "{img_title}")'
        text = self.CAROUSEL_OPEN_FENCE + image_string + self.CAROUSEL_CLOSE_FENCE

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        image_html = f'<img class="small-preview" alt="{img_alt}" src="{img_path}" title="{img_title}">'
        expected_output = BEFORE_CAROUSEL_HTML.format(0) + image_html + AFTER_CAROUSEL_HTML
        self.assertEqual(expected_output, html)

    def test_full_match_with_existing_class(self):
        """A carousel with images, one already specifying a classname"""
        img_alt = 'image text'
        img_title = 'image title'
        img_path = 'path/to/img.jpg'
        class_name = "extra-class"
        class_decl = '{@class=' + class_name + '}'
        image_string = f'![{img_alt}]({img_path} "{img_title}")'

        image_with_class = f'![{img_alt}{class_decl}]({img_path} "{img_title}")'
        text = self.CAROUSEL_OPEN_FENCE + image_string + image_with_class + self.CAROUSEL_CLOSE_FENCE

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        image_html = f'<img class="small-preview" alt="{img_alt}" src="{img_path}" title="{img_title}">' \
                     f'<img alt="{img_alt}" class="small-preview {class_name}" src="{img_path}" title="{img_title}">'
        expected_output = BEFORE_CAROUSEL_HTML.format(0) + image_html + AFTER_CAROUSEL_HTML
        self.assertEqual(expected_output, html)

    def test_multiple_subsequent_matches(self):
        """Multiple matches that are one after another"""
        img_alt = 'image text'
        img_title = 'image title'
        img_path = 'path/to/img.jpg'
        image_string = f'![{img_alt}]({img_path} "{img_title}")'
        text = self.CAROUSEL_OPEN_FENCE + image_string + self.CAROUSEL_CLOSE_FENCE
        text += text

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        image_html = f'<img class="small-preview" alt="{img_alt}" src="{img_path}" title="{img_title}">'
        expected_output = BEFORE_CAROUSEL_HTML + image_html + AFTER_CAROUSEL_HTML
        expected_output += expected_output
        self.assertEqual(expected_output.format(0, 1), html)

    def test_multiple_matches_dispersed(self):
        """Multiple matches separated by other markdown"""
        img_alt = 'image text'
        img_title = 'image title'
        img_path = 'path/to/img.jpg'
        image_string = f'![{img_alt}]({img_path} "{img_title}")'
        text = self.CAROUSEL_OPEN_FENCE + image_string + self.CAROUSEL_CLOSE_FENCE
        italic_text = "italics"
        italics = f'*{italic_text}*'
        text += italics + text

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        image_html = f'<img class="small-preview" alt="{img_alt}" src="{img_path}" title="{img_title}">'
        expected_output = BEFORE_CAROUSEL_HTML + image_html + AFTER_CAROUSEL_HTML
        expected_output += f"<em>{italic_text}</em>" + expected_output
        self.assertEqual(expected_output.format(0, 1), html)

    def test_no_closing_tag(self):
        """If the [!carousel] tag is missing, don't process the rest, keep wrapping paragraph tag"""
        img_alt = 'image text'
        img_title = 'image title'
        img_path = 'path/to/img.jpg'
        image_string = f'![{img_alt}]({img_path} "{img_title}")'
        text = self.CAROUSEL_OPEN_FENCE + image_string

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        image_html = f'<p><img alt="{img_alt}" src="{img_path}" title="{img_title}"></p>'
        expected_output = image_html
        self.assertEqual(expected_output, html)
