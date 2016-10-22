# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import markdown
import unittest

import os

from docdown.sequence import SequenceDiagramBlockPreprocessor

class IncludeExtensionTest(unittest.TestCase):
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
        expected_output = '<p>Test File:</p>\n<pre><code># Test\n\nContent\n</code></pre>'
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
        expected_output = '<p>Test File:</p>\n<pre><code># Test\n\nContent\n</code></pre>'
        self.assertEqual(html, expected_output)

    def test_json(self):
        text = ('Test JSON:\n'
                '+++ test.json')

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = (
            '<p>Test JSON:</p>\n<div class="codehilite"><pre><span></span><span class="p">{</span><span class="nt">'
            '&quot;test&quot;</span><span class="p">:</span> '
            '<span class="s2">&quot;content&quot;</span><span class="p">}</span>\n</pre></div>')
        self.assertEqual(html, expected_output)

    def test_html(self):
        text = '''Test HTML:
+++ test.html'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test HTML:</p>\n<div class="codehilite"><pre><span></span><span class="p">&lt;</span>\
<span class="nt">html</span><span class="p">&gt;&lt;</span><span class="nt">head</span><span class="p">&gt;&lt;/</span>\
<span class="nt">head</span><span class="p">&gt;&lt;</span><span class="nt">body</span><span class="p">&gt;&lt;</span>\
<span class="nt">h1</span><span class="p">&gt;</span>Test<span class="p">&lt;/</span><span class="nt">h1</span><span \
class="p">&gt;&lt;/</span><span class="nt">body</span><span class="p">&gt;&lt;/</span><span class="nt">html</span>\
<span class="p">&gt;</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_js(self):
        text = '''Test JS:
+++ test.js'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test JS:</p>\n<div class="codehilite"><pre><span></span><span class="nx">alert</span>\
<span class="p">(</span><span class="s1">&#39;test&#39;</span><span class="p">);</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_css(self):
        text = '''Test CSS:
+++ test.css'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test CSS:</p>\n<div class="codehilite"><pre><span></span><span class="nc">.lime</span>\
<span class="p">{</span>\n  <span class="nb">color</span><span class="o">:</span> <span class="m">#75D366</span><span \
class="p">;</span>\n<span class="p">}</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_obj_c(self):
        text = '''Test Objective C:
+++ test.m'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test Objective C:</p>\n<div class="codehilite"><pre><span></span><span class="cp">\
#import &lt;Foundation/Foundation.h&gt;</span>\n\n<span class="kt">int</span> <span class="nf">main</span> <span \
class="p">(</span><span class="kt">int</span> <span class="n">argc</span><span class="p">,</span> <span class="k">\
const</span> <span class="kt">char</span> <span class="o">*</span> <span class="n">argv</span><span class="p">[])\
</span>\n<span class="p">{</span>\n        <span class="n">NSAutoreleasePool</span> <span class="o">*</span><span \
class="n">pool</span> <span class="o">=</span> <span class="p">[[</span><span class="n">NSAutoreleasePool</span> <span \
class="n">alloc</span><span class="p">]</span> <span class="n">init</span><span class="p">];</span>\n        <span \
class="n">NSLog</span> <span class="p">(</span><span class="err">@</span><span class="s">&quot;Test&quot;</span><span \
class="p">);</span>\n        <span class="p">[</span><span class="n">pool</span> <span class="n">drain</span><span \
class="p">];</span>\n        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>\n<span \
class="p">}</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_swift(self):
        text = '''Test Swift:
+++ test.swift'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test Swift:</p>\n<div class="codehilite"><pre><span></span><span class="bp">print\
</span><span class="p">(</span><span class="s">&quot;Test&quot;</span><span class="p">)</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_java(self):
        text = '''Test JAVA:
+++ test.java'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test JAVA:</p>\n<div class="codehilite"><pre><span></span><span class="kd">public\
</span> <span class="kd">class</span> <span class="nc">TestJava</span><span class="o">{</span>\n\n    <span \
class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span \
class="o">(</span><span class="n">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)\
</span> <span class="o">{</span>\n        <span class="n">System</span><span class="o">.</span><span class="na">out\
</span><span class="o">.</span><span class="na">println</span><span class="o">(</span><span class="s">&quot;Test&quot;\
</span><span class="o">);</span>\n    <span class="o">}</span>\n\n<span class="o">}</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_cpp(self):
        text = '''Test C++:
+++ test.cpp'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test C++:</p>\n<div class="codehilite"><pre><span></span><span class="cp">#include\
</span> <span class="cpf">&lt;iostream&gt;</span><span class="cp"></span>\n\n<span class="k">using</span> <span \
class="k">namespace</span> <span class="n">std</span><span class="p">;</span>\n\n<span class="kt">int</span> <span \
class="nf">main</span><span class="p">()</span>\n<span class="p">{</span>\n\t<span class="n">cout</span> <span \
class="o">&lt;&lt;</span> <span class="s">&quot;Test&quot;</span> <span class="o">&lt;&lt;</span> <span class="n">endl\
</span><span class="p">;</span>\n\t<span class="k">return</span> <span class="mi">0</span><span class="p">;</span>\n\
<span class="p">}</span>\n</pre></div>'''
        self.assertEqual(html, expected_output)

    def test_csv(self):
        text = '''Test CSV:
+++ test.csv'''

        html = markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs=self.extension_configs,
            output_format='html5'
        )
        expected_output = '''<p>Test CSV:<br>\n<table><tr><th>Test 1</th><th>Test 2</th><th>Test 3</th></tr><tr><td>a\
</td><td>b</td><td>c</td></tr></table></p>'''
        self.assertEqual(html, expected_output)
