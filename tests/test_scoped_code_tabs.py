# flake8: noqa E501
import unittest

import markdown


class ScopedCodeTabsExtensionTest(unittest.TestCase):
    """
    Integration test with markdown for :class:`docdown.scoped_code_tabs.ScopedCodeTabsExtension`
    """
    MARKDOWN_EXTENSIONS = ['docdown.scoped_code_tabs']

    def test_mixed_code_blocks(self):
        """
        Tests mixed code blocks to ensure extension is only run on those with |~ ... ~| fences
        """
        text = """\
### A set of code tabs in Python and Java
[comment]: # (This should render as two code tabs)
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

### A regular, non-tabbed code block in Bash
[comment]: # (This should render as two, non-tabbed code blocks)
```bash
codeblockinfo() {
    echo("This would NOT be passed through markdown_fenced_code_tabs");
}
```

```clojure
(defn code-block-info []
   (println "This should also render as a normal code block"))
(hello-world)
```

#### (White-space fences are OK)
[comment]: # (This should render as two more fenced code tabs even with whitespace around the fences)
  |~
```html
<html>
<head></head>
<body>
    <p>Hello {{ greeting|default:"World" }}!</p>
</body>
</html>
```

```python
def hello_world(name: str = None):
    greeting = name or 'World'
    return f'Hello {greeting}!'
```
 ~|
"""
        expected_output = """\
<h3>A set of code tabs in Python and Java</h3>
<div class=md-fenced-code-tabs id=tab-tab-group-0><input name=tab-group-0 type=radio id=tab-group-0-0_python checked=checked class=code-tab data-lang=python aria-controls=tab-group-0-0_python-panel role=tab><label for=tab-group-0-0_python class=code-tab-label data-lang=python id=tab-group-0-0_python-label>Python</label><div class=code-tabpanel role=tabpanel data-lang=python id=tab-group-0-0_python-panel aria-labelledby=tab-group-0-0_python-label><pre><code class=python>def main():
    print(&quot;This would be passed through markdown_fenced_code_tabs&quot;)
</code></pre></div><input name=tab-group-0 type=radio id=tab-group-0-1_java class=code-tab data-lang=java aria-controls=tab-group-0-1_java-panel role=tab><label for=tab-group-0-1_java class=code-tab-label data-lang=java id=tab-group-0-1_java-label>Java</label><div class=code-tabpanel role=tabpanel data-lang=java id=tab-group-0-1_java-panel aria-labelledby=tab-group-0-1_java-label><pre><code class=java>public static void main(String[] args) {
    System.out.println(&quot;This would be passed through markdown_fenced_code_tabs&quot;);
}
</code></pre></div></div>

<h3>A regular, non-tabbed code block in Bash</h3>
<p><code>bash
codeblockinfo() {
    echo("This would NOT be passed through markdown_fenced_code_tabs");
}</code></p>
<p><code>clojure
(defn code-block-info []
   (println "This should also render as a normal code block"))
(hello-world)</code></p>
<h4>(White-space fences are OK)</h4>
<div class=md-fenced-code-tabs id=tab-tab-group-0><input name=tab-group-0 type=radio id=tab-group-0-0_html checked=checked class=code-tab data-lang=html aria-controls=tab-group-0-0_html-panel role=tab><label for=tab-group-0-0_html class=code-tab-label data-lang=html id=tab-group-0-0_html-label>Html</label><div class=code-tabpanel role=tabpanel data-lang=html id=tab-group-0-0_html-panel aria-labelledby=tab-group-0-0_html-label><pre><code class=html>&lt;html&gt;
&lt;head&gt;&lt;/head&gt;
&lt;body&gt;
    &lt;p&gt;Hello {{ greeting|default:&quot;World&quot; }}!&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre></div><input name=tab-group-0 type=radio id=tab-group-0-1_python class=code-tab data-lang=python aria-controls=tab-group-0-1_python-panel role=tab><label for=tab-group-0-1_python class=code-tab-label data-lang=python id=tab-group-0-1_python-label>Python</label><div class=code-tabpanel role=tabpanel data-lang=python id=tab-group-0-1_python-panel aria-labelledby=tab-group-0-1_python-label><pre><code class=python>def hello_world(name: str = None):
    greeting = name or 'World'
    return f'Hello {greeting}!'
</code></pre></div></div>"""

        html = markdown.markdown(
            text,
            extensions=['docdown.scoped_code_tabs'],
            output_format='html5')

        self.maxDiff = len(html) * 2
        self.assertEqual(html, expected_output)

    def test_custom_config_values(self):
        config = {
            'docdown.scoped_code_tabs': {
                'single_block_as_tab': True,
                'template': 'bootstrap4'
            }
        }

        text = """\
|~
```python
def hello_world(greeting: str = 'World'):
    return f'Hello {greeting}!'
```
 ~|
"""

        expected_output = """\
<p> <div class=md-fenced-code-tabs id=tab-tab-group-0><ul class="nav nav-tabs"><li class=nav-item><a class="nav-link active" href=#tab-group-0-0_python-panel role=tab id=tab-group-0-0_python-tab data-toggle=tab data-lang=python aria-controls=tab-group-0-0_python-panel aria-selected=true>Python</a></li></ul><div class=tab-content><div id=tab-group-0-0_python-panel class="tab-pane show active" role=tabpanel aria-labelledby=tab-group-0-0_python-tab><pre><code class=python>def hello_world(greeting: str = 'World'):
    return f'Hello {greeting}!'
</code></pre></div></div></div></p>"""

        html = markdown.markdown(
            text,
            extensions=['docdown.scoped_code_tabs'],
            extension_configs=config,
            output_format='html5')

        self.maxDiff = len(html) * 2
        self.assertEqual(html, expected_output)
