"""
scoped_code_tabs
----------------------------------

docdown.scoped_code_tabs Markdown extension module
"""

import re

from docdown.fenced_code_tabs import CodeTabsExtension, CodeTabsPreprocessor, util

RE_FENCE_START = re.compile(r"^ *\|\~\s*$")  # start line, e.g., `   |~  `
RE_FENCE_END = re.compile(r"^\s*\~\|\s*$")  # last non-blank line, e.g, '~|\n  \n\n'


class ScopedCodeTabsPreprocessor(CodeTabsPreprocessor):
    def pre_run_code_tab_preprocessor(self, lines):
        """
        Mark the code block for code tab pre-processing but hold off on rendering the tabs
            until all are processed so that the HTML tab group indexing will work properly in
            a global context
        """
        return self._parse_code_blocks("\n".join(lines))

    def run(self, lines):
        self.codehilite_config = self._get_codehilite_config()

        new_lines = []
        fenced_code_tab = []
        tab_break_line = "<!-- SCOPED_TAB_BREAK-->"
        starting_line = None
        in_tab = False

        for line in lines:
            if re.search(RE_FENCE_START, line):
                # Start block pattern, save line in case of no end fence
                in_tab = True
                starting_line = line
            elif re.search(RE_FENCE_END, line):
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
        return [line for line in self._render_code_tabs("\n".join(new_lines)).split("\n") if line != tab_break_line]


class ScopedCodeTabExtension(CodeTabsExtension):
    def __init__(self, *args, **kwargs):
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
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        self.setConfig("single_block_as_tab", util.to_bool(self.getConfig("single_block_as_tab")))

        template_file = self.getConfig("template")
        template_file_name = self._get_template_file_name(template_file)
        self.setConfig("template", template_file_name)

        md.registerExtension(self)

        md.preprocessors.register(ScopedCodeTabsPreprocessor(md, self.getConfigs()), "scoped_code_tabs", 26)


def makeExtension(*args, **kwargs):
    return ScopedCodeTabExtension(*args, **kwargs)
