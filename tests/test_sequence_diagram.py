# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import markdown
import unittest

from docdown.sequence import SequenceDiagramBlockPreprocessor


class SequenceDiagramExtensionTest(unittest.TestCase):
    """
    Primarily integration tests for the SequenceDiagramExtension
    """

    EXTENSION_CONFIGS = {
        'docdown.sequence': {
            'media_path': 'http://example.com/',
        }
    }

    MARKDOWN_EXTENSIONS = ['docdown.sequence']

    def test_sequence_diagram_with_media_path_and_relative_image_path(self):
        """
        Test a single sequence diagram renders correctly
        """
        text = ("# Sequence Diagrams\n"
                "|||\n"
                "Activate App after successful Resumption\n"
                "![Activate App Successful Resume](./assets/ActivateAppSuccessfulResume.png)\n"
                "|||")

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        expected_output = (
            '<h1>Sequence Diagrams</h1>\n'
            '<div class="visual-link-wrapper">'
            '<a href="#" data-src="http://example.com/assets/ActivateAppSuccessfulResume.png" class="visual-link">'
            '<div class="visual-link__body"><div class="t-h6 visual-link__title">Sequence Diagram</div>'
            '<p class="t-default">\n\n'
            '<p>Activate App after successful Resumption</p>\n'
            '<p></p></div><div class="visual-link__link fx-wrapper fx-s-between fx-a-center">'
            '<span class="fc-theme">View Diagram</span><span class="icon">{% svg "standard/icon-visual" %}</span>'
            '</div></a></div>\n'
            '<img class="visual-print-image" src="http://example.com/assets/ActivateAppSuccessfulResume.png"></p>')
        self.assertEqual(html, expected_output)

    def test_sequence_diagram_default_media_path(self):
        """
        Test that the URL gets the default `.` prepended, making it a relative path
        """
        text = ("# Sequence Diagrams\n"
                "|||\n"
                "Activate App after successful Resumption\n"
                "![Activate App Successful Resume](/assets/ActivateAppSuccessfulResume.png)\n"
                "|||")

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        expected_output = (
            '<h1>Sequence Diagrams</h1>\n'
            '<div class="visual-link-wrapper">'
            '<a href="#" data-src="./assets/ActivateAppSuccessfulResume.png" class="visual-link">'
            '<div class="visual-link__body"><div class="t-h6 visual-link__title">Sequence Diagram</div>'
            '<p class="t-default">\n\n'
            '<p>Activate App after successful Resumption</p>\n'
            '<p></p></div><div class="visual-link__link fx-wrapper fx-s-between fx-a-center">'
            '<span class="fc-theme">View Diagram</span><span class="icon">{% svg "standard/icon-visual" %}</span>'
            '</div></a></div>\n'
            '<img class="visual-print-image" src="./assets/ActivateAppSuccessfulResume.png"></p>')
        self.assertEqual(html, expected_output)

    def test_multiple_sequence_diagrams(self):
        """
        Test that multiple sequence diagrams in a row render correctly
        """
        text = ('# Sequence Diagrams\n'
               '|||\n'
               'multiple App after successful Resumption\n'
               '![Activate App Successful Resume](./assets/ActivateAppSuccessfulResume.png)\n'
               '|||\n\n'
               '|||\n'
               'asdf App after successful Resumption\n'
               '![Activate App Successful Resume](./assets/ActivateAppSuccessfulResume.png)\n'
               '|||')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        expected_output = (
            '<h1>Sequence Diagrams</h1>\n<div class="visual-link-wrapper">'
            '<a href="#" data-src="http://example.com/assets/ActivateAppSuccessfulResume.png" class="visual-link">'
            '<div class="visual-link__body"><div class="t-h6 visual-link__title">Sequence Diagram</div>'
            '<p class="t-default">\n\n<p>multiple App after successful Resumption</p>\n<p></p></div>'
            '<div class="visual-link__link fx-wrapper fx-s-between fx-a-center">'
            '<span class="fc-theme">View Diagram</span><span class="icon">{% svg "standard/icon-visual" %}</span></div>'
            '</a></div>\n'
            '<img class="visual-print-image" src="http://example.com/assets/ActivateAppSuccessfulResume.png"></p>\n'
            '<div class="visual-link-wrapper">'
            '<a href="#" data-src="http://example.com/assets/ActivateAppSuccessfulResume.png" class="visual-link">'
            '<div class="visual-link__body">'
            '<div class="t-h6 visual-link__title">Sequence Diagram</div><p class="t-default">\n\n'
            '<p>asdf App after successful Resumption</p>\n<p></p></div>'
            '<div class="visual-link__link fx-wrapper fx-s-between fx-a-center">'
            '<span class="fc-theme">View Diagram</span>'
            '<span class="icon">{% svg "standard/icon-visual" %}</span></div></a></div>\n'
            '<img class="visual-print-image" src="http://example.com/assets/ActivateAppSuccessfulResume.png"></p>')
        self.assertEqual(html, expected_output)


class SequenceDiagramBlockPreprocessorTest(unittest.TestCase):
    """
    Specifically test the preprocessor used by SequenceDiagramExtension.
    """
    
    def test_run_method_with_media_path(self):
        """
        When media_path is passed in, urls should be replaced with the media_path url.
        Placeholders should get properly replaced.  Each line in list of text should be treated as new line.
        """
        processor = SequenceDiagramBlockPreprocessor(media_path='http://example.com/', markdown_instance=markdown.Markdown())
        text = ("# Sequence Diagrams",
                "|||",
                "Activate App after successful Resumption",
                "![Activate App Successful Resume](./assets/ActivateAppSuccessfulResume.png)",
                "|||",)
        processed = processor.run(text)

        # placeholder pipes are replaced with a code
        # each element in the list is treated as a line and so a newline is inserted
        # adding an extra empty line between each element
        expected = ['# Sequence Diagrams', '',
                '\x02wzxhzdk:0\x03',
                '',
                'Activate App after successful Resumption', '',
                '\x02wzxhzdk:1\x03',
                '<img class="visual-print-image" src="http://example.com/assets/ActivateAppSuccessfulResume.png">',
                ''
                ]
        self.assertEqual(processed, expected)

    def test_run_method_without_path_and_relative_sequence_file_path_given(self):
        """
        If no media_path and a relative file path is given, the leading ./ should be stripped from
        the path to the sequence diagram image.
        Placeholders should get properly replaced.  Each line in list of text should be treated as new line.
        """
        processor = SequenceDiagramBlockPreprocessor(markdown_instance=markdown.Markdown())
        text = ("# Sequence Diagrams",
                "|||",
                "Activate App after successful Resumption",
                "![Activate App Successful Resume](./assets/ActivateAppSuccessfulResume.png)",
                "|||",)
        processed = processor.run(text)

        # placeholder pipes are replaced with a code
        # each element in the list is treated as a line and so a newline is inserted
        # adding an extra empty line between each element
        expected = ['# Sequence Diagrams', '',
                '\x02wzxhzdk:0\x03',
                '',
                'Activate App after successful Resumption', '',
                '\x02wzxhzdk:1\x03',
                '<img class="visual-print-image" src="assets/ActivateAppSuccessfulResume.png">',
                ''
                ]
        self.assertEqual(processed, expected)

    def test_run_method_without_path_and_absolute_sequence_file_path_given(self):
        """
        If no media_path and an absolute file path is given, the leading ./ should be stripped from
        the path to the sequence diagram image.
        Placeholders should get properly replaced.  Each line in list of text should be treated as new line.
        """
        processor = SequenceDiagramBlockPreprocessor(markdown_instance=markdown.Markdown())
        text = ("# Sequence Diagrams",
                "|||",
                "Activate App after successful Resumption",
                "![Activate App Successful Resume](/assets/ActivateAppSuccessfulResume.png)",
                "|||",)
        processed = processor.run(text)

        # placeholder pipes are replaced with a code
        # each element in the list is treated as a line and so a newline is inserted
        # adding an extra empty line between each element
        expected = ['# Sequence Diagrams', '',
                '\x02wzxhzdk:0\x03',
                '',
                'Activate App after successful Resumption', '',
                '\x02wzxhzdk:1\x03',
                '<img class="visual-print-image" src="/assets/ActivateAppSuccessfulResume.png">',
                ''
                ]
        self.assertEqual(processed, expected)
