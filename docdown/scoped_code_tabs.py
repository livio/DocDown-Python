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

    def pre_run_code_tab_preprocessor(self, lines):
        """
        Mark the code block for code tab pre-processing but hold off on rendering the tabs
            until all are processed so that the HTML tab group indexing will work properly in
            a global context
        """
        self.code_tabs_preprocessor.codehilite_config = self.code_tabs_preprocessor._get_codehilite_config()
        return self.code_tabs_preprocessor._parse_code_blocks('\n'.join(lines))

    def run(self, lines):
        new_lines = []
        fenced_code_tab = []
        tab_break_line = "<!-- SCOPED_TAB_BREAK-->"
        starting_line = None
        in_tab = False

        for line in lines:
            if re.search(self.RE_FENCE_START, line):
                # Start block pattern, save line in case of no end fence
                in_tab = True
                starting_line = line
            elif re.search(self.RE_FENCE_END, line):
                # End of code block, run through fenced code tabs pre-processor and reset code tab list
                # Add <!-- SCOPED_TAB_BREAK--> content break to separate potentially subsequent tab groups
                new_lines.append(tab_break_line)
                new_lines.append(self.pre_run_code_tab_preprocessor(fenced_code_tab))
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

        # Finally, run the whole thing through the code tabs rendering function
        return [line for line in self.code_tabs_preprocessor._render_code_tabs('\n'.join(new_lines)).split('\n') if
                line != tab_break_line]


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
        # The parent class will replace the fenced_code_block preprocessor in its extendMarkdown.
        #   In order for this to be truly a scoped extension, we need to replace it back with the base
        #   if one exists, or remove it entirely.
        if 'fenced_code_block' in md.preprocessors:
            base_fenced_code_preprocessor = md.preprocessors.get('fenced_code_block')
            super(ScopedCodeTabExtension, self).extendMarkdown(md, md_globals)

            code_tabs_preprocessor = md.preprocessors['fenced_code_block']
            md.preprocessors['fenced_code_block'] = base_fenced_code_preprocessor
        else:
            super(ScopedCodeTabExtension, self).extendMarkdown(md, md_globals)
            code_tabs_preprocessor = md.preprocessors['fenced_code_block']
            del md.preprocessors['fenced_code_block']

        md.registerExtension(self)

        md.preprocessors.add('scoped_code_tabs',
                             ScopedCodeTabsPreprocessor(md,
                                                        code_tabs_preprocessor=code_tabs_preprocessor),
                             ">normalize_whitespace")


def makeExtension(*args, **kwargs):
    return ScopedCodeTabExtension(*args, **kwargs)
