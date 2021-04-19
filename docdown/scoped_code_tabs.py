# -*- coding: utf-8 -*-

"""
scoped_code_tabs
----------------------------------

docdown.scoped_code_tabs Markdown extension module
"""
import re

from markdown.preprocessors import Preprocessor
from markdown_fenced_code_tabs import CodeTabsExtension


class ScopedCodeTabsPreprocessor(Preprocessor):
    RE_FENCE_START = r'^ *\|\~\s*$'  # start line, e.g., `   |~  `
    RE_FENCE_END = r'^\s*\~\|\s*$'  # last non-blank line, e.g, '~|\n  \n\n'

    def __init__(self, md, code_tabs_preprocessor):
        self.code_tabs_preprocessor = code_tabs_preprocessor
        super(ScopedCodeTabsPreprocessor, self).__init__(md)

    def run(self, lines):
        new_lines = []
        fenced_code_tab = []
        starting_line = None
        in_tab = False

        for line in lines:
            if re.search(self.RE_FENCE_START, line):
                # Start block pattern, save line in case of no end fence
                in_tab = True
                starting_line = line
            elif re.search(self.RE_FENCE_END, line):
                # End of code block, run through fenced code tabs pre-processor and reset code tab list
                new_lines += self.code_tabs_preprocessor.run(fenced_code_tab)
                fenced_code_tab = []
                in_tab = False
            elif in_tab:
                # Still in tab -- append to tab list
                fenced_code_tab.append(line)
            else:
                # Not in a fenced code tab, and not starting/ending one -- pass as usual
                new_lines.append(line)

        # Non-terminated code tab block, append matching starting fence and remaining lines without processing
        if fenced_code_tab:
            new_lines += [starting_line] + fenced_code_tab
        return new_lines


class ScopedCodeTabExtension(CodeTabsExtension):

    def __init__(self, **kwargs):
        """
        A Markdown extension that serves to scope where Fenced Code Tabs are rendered by way of |~ ... ~| fences.

        Example:

    ## A set of code tabs in Python and Java
    |~
    ```python
    def main():
        print("This would be passed through markdown_fenced_code_tabs")
    ```

    ```java
    public static void main(String[] args) {
        System.out.println("This would be passed through markdown_fenced_code_tabs");
    }
    ```
    ~|

    ## A regular, non-tabbed code block in Bash
    ```bash
    codeblockinfo() {
        echo("This would NOT be passed through markdown_fenced_code tabs");
    }
    ```
        """
        super(ScopedCodeTabExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        super(ScopedCodeTabExtension, self).extendMarkdown(md, md_globals)
        md.registerExtension(self)

        md.preprocessors.add('scoped_code_tabs',
                             ScopedCodeTabsPreprocessor(md,
                                                        code_tabs_preprocessor=md.preprocessors['fenced_code_block']),
                             ">normalize_whitespace")
        del md.preprocessors['fenced_code_block']


def makeExtension(*args, **kwargs):
    return ScopedCodeTabExtension(*args, **kwargs)
