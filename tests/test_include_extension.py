# -*- coding: utf-8 -*-

"""
test_include_extension
----------------------------------

Tests for `docdown.include` module.
"""

from __future__ import absolute_import, unicode_literals, print_function

import markdown
import unittest

import os

from docdown.include import IncludePreprocessor

class IncludeExtensionTest(unittest.TestCase):
    """
    Test the IncludeExtension.

    Primarily runs as an integration test by using it with markdown.  This test includes the `fenced_code`
    extension because the current output from the preprocessor assumes the `fenced_code` extension will
    be in use.
    """
    # TODO: This test appears to be relying on behavior from another extension
    # due to the expected output vs what is really being output... nl2br and fenced_code
    # The extension should probably check for them, or at least document that they are needed,
    # if they are expected to always be there.
    _root = os.path.dirname(os.path.abspath(__file__))
    ASSET_DIR = os.path.join(_root, 'test_files', 'assets')

    MARKDOWN_EXTENSIONS = [
        'markdown.extensions.fenced_code',
        'docdown.include']

    EXTENSION_CONFIGS = {
        'docdown.include': {
            'asset_directory': ASSET_DIR,
            'root_directory': ASSET_DIR,
        }
    }

    def test_text_with_extension_default_config(self):
        text = ('Test File:\n' '+++ %s/test.md' % self.ASSET_DIR)

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        # TODO: Expected output with code_block and nl2br and codehilite extensions
        # Are any of these truly expected to always be used with this extension?
        # expected_output = ('<p>Test File:</p>\n<div class="codehilite">'
        #                    '<pre><span></span># Test\n\nContent\n</pre>#</div>')
        expected_output = (
            '<p>Test File:</p>\n'
            '<pre><code># Test\n\n'
            'Content\n'
            '</code></pre>')
        self.assertEqual(html, expected_output)

    def test_text_with_set_asset_dir(self):
        text = ('Test File:\n' '+++ test.md')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # TODO: Expected output with code_block and nl2br and codehilite extensions
        # Are any of these truly expected to always be used with this extension?
        # expected_output = ('<p>Test File:</p>\n<div class="codehilite"><pre><span></span>'
        #                    '# Test\n\nContent\n</pre>\n</div>')
        expected_output = (
            '<p>Test File:</p>\n'
            '<pre><code># Test\n\n'
            'Content\n'
            '</code></pre>')
        self.assertEqual(html, expected_output)

    def test_json(self):
        text = ('Test JSON:\n'
                '+++ test.json')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        expected_output = ('<p>Test JSON:</p>\n'
                           '<pre><code class="json">{&quot;test&quot;: &quot;content&quot;}\n'
                           '</code></pre>')

        # output with codehilite, nl2br, and fenced_code
        # expected_output = (
        #     '<p>Test JSON:</p>\n<div class="codehilite"><pre><span></span><span class="p">{</span><span class="nt">'
        #     '&quot;test&quot;</span><span class="p">:</span> '
        #     '<span class="s2">&quot;content&quot;</span><span class="p">}</span>\n</pre></div>')
        self.assertEqual(html, expected_output)

    def test_html(self):
        text = ('Test HTML:\n'
                '+++ test.html')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # output with codehilite, nl2br, and fenced_code
        # expected_output = (
        #     '<p>Test HTML:</p>\n<div class="codehilite"><pre><span></span><span class="p">&lt;</span>'
        #     '<span class="nt">html</span><span class="p">&gt;&lt;</span><span class="nt">head</span>'
        #     '<span class="p">&gt;&lt;/</span><span class="nt">head</span><span class="p">&gt;&lt;</span>'
        #     '<span class="nt">body</span><span class="p">&gt;&lt;</span><span class="nt">h1</span>'
        #     '<span class="p">&gt;</span>Test<span class="p">&lt;/</span><span class="nt">h1</span>'
        #     '<span class="p">&gt;&lt;/</span><span class="nt">body</span><span class="p">&gt;&lt;/</span>'
        #     '<span class="nt">html</span><span class="p">&gt;</span>\n</pre></div>')

        expected_output = (
            '<p>Test HTML:</p>\n'
            '<pre><code class="html">&lt;html&gt;&lt;head&gt;&lt;/head&gt;&lt;'
            'body&gt;&lt;h1&gt;Test&lt;/h1&gt;&lt;/body&gt;&lt;/html&gt;\n'
            '</code></pre>')

        self.assertEqual(html, expected_output)

    def test_js(self):
        text = ('Test JS:\n'
                '+++ test.js')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )
        # output with codehilite, nl2br, and fenced_code
        # expected_output = '''<p>Test JS:</p>\n<div class="codehilite"><pre><span></span><span class="nx">alert</span>\
# <span class="p">(</span><span class="s1">&#39;test&#39;</span><span class="p">);</span>\n</pre></div>'''

        expected_output = (
            '<p>Test JS:</p>\n'
            '''<pre><code class="javascript">alert('test');\n'''
            '</code></pre>')
        self.assertEqual(html, expected_output)

    def test_css(self):
        text = ('Test CSS:\n'
                '+++ test.css')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )
        # output with codehilite, nl2br, and fenced_code
#         expected_output = '''<p>Test CSS:</p>\n<div class="codehilite"><pre><span></span><span class="nc">.lime</span>\
# <span class="p">{</span>\n  <span class="nb">color</span><span class="o">:</span> <span class="m">#75D366</span><span \
# class="p">;</span>\n<span class="p">}</span>\n</pre></div>'''

        expected_output = ('<p>Test CSS:</p>\n'
                           '<pre><code class="css">.lime{\n'
                           '  color: #75D366;\n'
                           '}\n'
                           '</code></pre>')

        self.assertEqual(html, expected_output)

    def test_obj_c(self):
        text = ('Test Objective C:\n'
                '+++ test.m')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # output with codehilite, nl2br, and fenced_code
#         expected_output = '''<p>Test Objective C:</p>\n<div class="codehilite"><pre><span></span><span class="cp">\
# #import &lt;Foundation/Foundation.h&gt;</span>\n\n<span class="kt">int</span> <span class="nf">main</span> <span \
# class="p">(</span><span class="kt">int</span> <span class="n">argc</span><span class="p">,</span> <span class="k">\
# const</span> <span class="kt">char</span> <span class="o">*</span> <span class="n">argv</span><span class="p">[])\
# </span>\n<span class="p">{</span>\n        <span class="n">NSAutoreleasePool</span> <span class="o">*</span><span \
# class="n">pool</span> <span class="o">=</span> <span class="p">[[</span><span class="n">NSAutoreleasePool</span> <span \
# class="n">alloc</span><span class="p">]</span> <span class="n">init</span><span class="p">];</span>\n        <span \
# class="n">NSLog</span> <span class="p">(</span><span class="err">@</span><span class="s">&quot;Test&quot;</span><span \
# class="p">);</span>\n        <span class="p">[</span><span class="n">pool</span> <span class="n">drain</span><span \
# class="p">];</span>\n        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>\n<span \
# class="p">}</span>\n</pre></div>'''

        expected_output = (
            '<p>Test Objective C:</p>\n'
            '<pre><code class="c">#import &lt;Foundation/Foundation.h&gt;'
            '\n\nint main (int argc, const char * argv[])\n{\n'
            '        NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];\n'
            '        NSLog (@&quot;Test&quot;);\n'
            '        [pool drain];\n'
            '        return 0;\n}\n'
            '</code></pre>')

        self.assertEqual(html, expected_output)

    def test_swift(self):
        text = ('Test Swift:\n'
                '+++ test.swift')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # output with codehilite, nl2br, and fenced_code
        # expected_output = (
        #     '<p>Test Swift:</p>\n<div class="codehilite"><pre><span></span><span class="bp">print</span>'
        #     '<span class="p">(</span><span class="s">&quot;Test&quot;</span><span class="p">)</span>\n</pre></div>')

        expected_output = (
            '<p>Test Swift:</p>\n'
            '<pre><code class="swift">print(&quot;Test&quot;)\n'
            '</code></pre>')

        self.assertEqual(html, expected_output)

    def test_java(self):
        text = ('Test JAVA:\n'
                '+++ test.java')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # output with codehilite, nl2br, and fenced_code
        # expected_output = (
        #     '<p>Test JAVA:</p>\n<div class="codehilite"><pre><span></span><span class="kd">public</span>'
        #     ' <span class="kd">class</span> <span class="nc">TestJava</span><span class="o">{</span>\n\n'
        #     '    <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> '
        #     '<span class="nf">main</span><span class="o">(</span><span class="n">String</span><span class="o">[]</span>'
        #     ' <span class="n">args</span><span class="o">)</span> <span class="o">{</span>\n'
        #     '        <span class="n">System</span><span class="o">.</span><span class="na">out</span>'
        #     '<span class="o">.</span><span class="na">println</span><span class="o">'
        #     '(</span><span class="s">&quot;Test&quot;</span><span class="o">);</span>\n'
        #     '    <span class="o">}</span>\n\n<span class="o">}</span>\n</pre></div>')

        expected_output = (
            '<p>Test JAVA:</p>\n'
            '<pre><code class="java">public class TestJava{\n\n'
            '    public static void main(String[] args) {\n'
            '        System.out.println(&quot;Test&quot;);\n'
            '    }\n\n'
            '}\n'
            '</code></pre>')

        self.assertEqual(html, expected_output)

    def test_cpp(self):
        text = ('Test C++:\n'
                '+++ test.cpp')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # output with codehilite, nl2br, and fenced_code
        # expected_output = (
        #     '<p>Test C++:</p>\n'
        #     '<div class="codehilite"><pre><span></span><span class="cp">#include</span> '
        #     '<span class="cpf">&lt;iostream&gt;</span><span class="cp"></span>\n\n<span class="k">using</span> '
        #     '<span class="k">namespace</span> <span class="n">std</span><span class="p">;</span>\n\n'
        #     '<span class="kt">int</span> <span class="nf">main</span><span class="p">()</span>\n'
        #     '<span class="p">{</span>\n\t<span class="n">cout</span> <span class="o">&lt;&lt;</span> '
        #     '<span class="s">&quot;Test&quot;</span> <span class="o">&lt;&lt;</span> <span class="n">endl</span>'
        #     '<span class="p">;</span>\n'
        #     '\t<span class="k">return</span> <span class="mi">0</span><span class="p">;</span>\n'
        #     '<span class="p">}</span>\n'
        #     '</pre></div>')

        expected_output = (
            '<p>Test C++:</p>\n'
            '<pre><code class="cpp">#include &lt;iostream&gt;\n\n'
            'using namespace std;\n\n'
            'int main()\n'
            '{\n'
            '\tcout &lt;&lt; &quot;Test&quot; &lt;&lt; endl;\n'
            '\treturn 0;\n'
            '}\n'
            '</code></pre>')
        self.assertEqual(html, expected_output)

    def test_csv(self):
        text = ('Test CSV:\n'
                '+++ test.csv')

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
            output_format='html5'
        )

        # output with codehilite, nl2br, and fenced_code
        # expected_output = (
        #     '<p>Test CSV:<br>\n'
        #     '<table><tr><th>Test 1</th><th>Test 2</th><th>Test 3</th></tr>'
        #     '<tr><td>a</td><td>b</td><td>c</td></tr></table></p>')
        expected_output = (
            '<p>Test CSV:\n'
            '<table><tr><th>Test 1</th><th>Test 2</th><th>Test 3</th></tr>'
            '<tr><td>a</td><td>b</td><td>c</td></tr></table></p>')

        self.assertEqual(html, expected_output)


class IncludePreprocessorTest(unittest.TestCase):
    """
    Test the IncludePreprocessor
    """

    def test_find_file_path(self):
        pass

    def test_handle_csv(self):
        pass

    def test_handle_code_default(self):
        pass

    def test_handle_code_json(self):
        # TODO: write one for each language
        pass

    def test_handle_code_javascript(self):
        # TODO: write one for each language
        pass

    def test_handle_code_java(self):
        # TODO: write one for each language
        pass

    def test_handle_code_c(self):
        # TODO: write one for each language
        pass

    def test_handle_code_html(self):
        # TODO: write one for each language
        pass

    def test_handle_code_text(self):
        # TODO: write one for each language
        pass

    def test_handle_code_swift(self):
        # TODO: write one for each language
        pass

    def test_handle_code_css(self):
        # TODO: write one for each language
        pass

    def test_handle_code_cpp(self):
        # TODO: write one for each language
        pass
