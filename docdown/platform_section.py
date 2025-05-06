"""
platform_section
----------------------------------

docdown.platform_section Markdown extension module
"""

import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class PlatformSectionPreprocessor(Preprocessor):
    PLATFORM_SECTION_RE = re.compile(r"""@!\[(?P<sections>[\w, ]+)\](?P<content>.*?)!@""", re.DOTALL | re.VERBOSE)

    STARTSWITH_WHITESPACE_RE = re.compile(r"^\W+(@!\[|\n)")
    MULTI_NEWLINE_RE = re.compile(r"^(\n){2,}")

    def __init__(self, platform_section, **kwargs):
        self.platform_section = platform_section.lower().strip()
        super().__init__(**kwargs)

    def run(self, lines):
        text = "\n".join(lines)
        text = self.process_platform_sections(text)
        return text.split("\n")

    def split_sections(self, sections_group):
        return [section.lower().strip() for section in sections_group.split(",")]

    def process_platform_sections(self, text):
        while 1:
            m = self.PLATFORM_SECTION_RE.search(text)
            if m:
                sections = self.split_sections(m.group("sections"))

                start = text[: m.start()]
                end = text[m.end() :]
                if self.STARTSWITH_WHITESPACE_RE.match(end):
                    if self.MULTI_NEWLINE_RE.match(end):
                        end = "\n" + end.lstrip()
                    else:
                        end = end.lstrip()

                if self.platform_section in sections:
                    content = m.group("content")
                    text = "{}{}{}".format(start, content, end)
                else:
                    text = "{}{}".format(start, end)
            else:
                break
        return text


class PlatformSectionExtension(Extension):
    """
    Renders a block of content if and only if the configured platform section is in the DocDown tag's list of platform
    sections.

    Configuration Example:
    {
        'platform_section': 'Android',
    }
    """

    def __init__(self, **kwargs):
        self.config = {
            "platform_section": ["", "The platform section that should be rendered."],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """Add NoteBlockPreprocessor to the Markdown instance."""
        md.registerExtension(self)

        platform_section = self.getConfig("platform_section")

        md.preprocessors.register(
            PlatformSectionPreprocessor(platform_section=platform_section, md=md),
            "platform_sections",
            31,  # after normalize_whitespace
        )


def makeExtension(*args, **kwargs):
    return PlatformSectionExtension(*args, **kwargs)
