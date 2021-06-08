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
        Tests tabbed and non-tabbed code blocks to ensure extension is only run on those with |~ ... ~| fences
            and that the indexing on tabbed HTML classes works correctly
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

<p><code>bash
codeblockinfo() {
    echo("This would NOT be passed through markdown_fenced_code_tabs");
}</code>
<code>clojure
(defn code-block-info []
   (println "This should also render as a normal code block"))
(hello-world)</code></p>
<div class=md-fenced-code-tabs id=tab-tab-group-1><input name=tab-group-1 type=radio id=tab-group-1-0_html checked=checked class=code-tab data-lang=html aria-controls=tab-group-1-0_html-panel role=tab><label for=tab-group-1-0_html class=code-tab-label data-lang=html id=tab-group-1-0_html-label>Html</label><div class=code-tabpanel role=tabpanel data-lang=html id=tab-group-1-0_html-panel aria-labelledby=tab-group-1-0_html-label><pre><code class=html>&lt;html&gt;
&lt;head&gt;&lt;/head&gt;
&lt;body&gt;
    &lt;p&gt;Hello {{ greeting|default:&quot;World&quot; }}!&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</code></pre></div><input name=tab-group-1 type=radio id=tab-group-1-1_python class=code-tab data-lang=python aria-controls=tab-group-1-1_python-panel role=tab><label for=tab-group-1-1_python class=code-tab-label data-lang=python id=tab-group-1-1_python-label>Python</label><div class=code-tabpanel role=tabpanel data-lang=python id=tab-group-1-1_python-panel aria-labelledby=tab-group-1-1_python-label><pre><code class=python>def hello_world(name: str = None):
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

    def test_fenced_code_mixed_hilite_and_fenced_code(self):
        """
        Tests that the base fenced_code_block preprocessor is not replaced by code tabs
            and that the hilite library is properly loaded when used
        """
        text = """\
|~
```objc
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // insert code here...
        NSLog(@"Hello, World!");
    }
    return 0;
}
```
```swift
// Hello, World! Program
import Swift
print("Hello, World!")
```
~|
```xml
<interface name="string" version="string" minVersion="string" date="string">
  <!--Zero or more repetitions:-->
  <enum/>
  <!--Zero or more repetitions:-->
  <struct/>
  <!--Zero or more repetitions:-->
  <function/>
</interface>
```
```xml
<interface name="string" version="string" minVersion="string" date="string">
  <!--Zero or more repetitions:-->
  <enum/>
  <!--Zero or more repetitions:-->
  <struct/>
  <!--Zero or more repetitions:-->
  <function/>
</interface>
```
"""

        html = markdown.markdown(
            text,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'docdown.scoped_code_tabs',
            ],
            output_format='html5')

        expected_output = """\
<div class=md-fenced-code-tabs id=tab-tab-group-0><input name=tab-group-0 type=radio id=tab-group-0-0_objc checked=checked class=code-tab data-lang=objc aria-controls=tab-group-0-0_objc-panel role=tab><label for=tab-group-0-0_objc class=code-tab-label data-lang=objc id=tab-group-0-0_objc-label>Objc</label><div class=code-tabpanel role=tabpanel data-lang=objc id=tab-group-0-0_objc-panel aria-labelledby=tab-group-0-0_objc-label><div class=codehilite><pre><span></span><span class=cp>#import &lt;Foundation/Foundation.h&gt;</span>

<span class=kt>int</span> <span class=nf>main</span><span class=p>(</span><span class=kt>int</span> <span class=n>argc</span><span class=p>,</span> <span class=k>const</span> <span class=kt>char</span> <span class=o>*</span> <span class=n>argv</span><span class=p>[])</span> <span class=p>{</span>
    <span class=k>@autoreleasepool</span> <span class=p>{</span>
        <span class=c1>// insert code here...</span>
        <span class=n>NSLog</span><span class=p>(</span><span class=s>@&quot;Hello, World!&quot;</span><span class=p>);</span>
    <span class=p>}</span>
    <span class=k>return</span> <span class=mi>0</span><span class=p>;</span>
<span class=p>}</span>
</pre></div></div><input name=tab-group-0 type=radio id=tab-group-0-1_swift class=code-tab data-lang=swift aria-controls=tab-group-0-1_swift-panel role=tab><label for=tab-group-0-1_swift class=code-tab-label data-lang=swift id=tab-group-0-1_swift-label>Swift</label><div class=code-tabpanel role=tabpanel data-lang=swift id=tab-group-0-1_swift-panel aria-labelledby=tab-group-0-1_swift-label><div class=codehilite><pre><span></span><span class=c1>// Hello, World! Program</span>
<span class=kd>import</span> <span class=nc>Swift</span>
<span class=bp>print</span><span class=p>(</span><span class=s>&quot;Hello, World!&quot;</span><span class=p>)</span>
</pre></div></div></div>

<div class="codehilite"><pre><span></span><span class="nt">&lt;interface</span> <span class="na">name=</span><span class="s">&quot;string&quot;</span> <span class="na">version=</span><span class="s">&quot;string&quot;</span> <span class="na">minVersion=</span><span class="s">&quot;string&quot;</span> <span class="na">date=</span><span class="s">&quot;string&quot;</span><span class="nt">&gt;</span>
  <span class="c">&lt;!--Zero or more repetitions:--&gt;</span>
  <span class="nt">&lt;enum/&gt;</span>
  <span class="c">&lt;!--Zero or more repetitions:--&gt;</span>
  <span class="nt">&lt;struct/&gt;</span>
  <span class="c">&lt;!--Zero or more repetitions:--&gt;</span>
  <span class="nt">&lt;function/&gt;</span>
<span class="nt">&lt;/interface&gt;</span>
</pre></div>


<div class="codehilite"><pre><span></span><span class="nt">&lt;interface</span> <span class="na">name=</span><span class="s">&quot;string&quot;</span> <span class="na">version=</span><span class="s">&quot;string&quot;</span> <span class="na">minVersion=</span><span class="s">&quot;string&quot;</span> <span class="na">date=</span><span class="s">&quot;string&quot;</span><span class="nt">&gt;</span>
  <span class="c">&lt;!--Zero or more repetitions:--&gt;</span>
  <span class="nt">&lt;enum/&gt;</span>
  <span class="c">&lt;!--Zero or more repetitions:--&gt;</span>
  <span class="nt">&lt;struct/&gt;</span>
  <span class="c">&lt;!--Zero or more repetitions:--&gt;</span>
  <span class="nt">&lt;function/&gt;</span>
<span class="nt">&lt;/interface&gt;</span>
</pre></div>"""

        self.maxDiff = len(html) * 2
        self.assertEqual(html, expected_output)

    def test_subsequent_scoped_code_tabs(self):
        """
        Two scoped code tab groups in direct succession with nothing in-between should still result in
            two distinct tab groups
        """
        text = """\
|~
```objc
- (void)hmiLevel:(SDLHMILevel)oldLevel didChangeToLevel:(SDLHMILevel)newLevel {
}
```
```swift
fileprivate var firstHMILevel: SDLHMILevel = .none
func hmiLevel(_ oldLevel: SDLHMILevel, didChangeToLevel newLevel: SDLHMILevel) {
}
```
~|
|~
```objc
- (void)hmiLevel:(SDLHMILevel)oldLevel didChangeToLevel:(SDLHMILevel)newLevel {
}
```
```swift
fileprivate var firstHMILevel: SDLHMILevel = .none
func hmiLevel(_ oldLevel: SDLHMILevel, didChangeToLevel newLevel: SDLHMILevel) {
}
```
~|
"""
        expected_output = """\
<div class=md-fenced-code-tabs id=tab-tab-group-0><input name=tab-group-0 type=radio id=tab-group-0-0_objc checked=checked class=code-tab data-lang=objc aria-controls=tab-group-0-0_objc-panel role=tab><label for=tab-group-0-0_objc class=code-tab-label data-lang=objc id=tab-group-0-0_objc-label>Objc</label><div class=code-tabpanel role=tabpanel data-lang=objc id=tab-group-0-0_objc-panel aria-labelledby=tab-group-0-0_objc-label><pre><code class=objc>- (void)hmiLevel:(SDLHMILevel)oldLevel didChangeToLevel:(SDLHMILevel)newLevel {
}
</code></pre></div><input name=tab-group-0 type=radio id=tab-group-0-1_swift class=code-tab data-lang=swift aria-controls=tab-group-0-1_swift-panel role=tab><label for=tab-group-0-1_swift class=code-tab-label data-lang=swift id=tab-group-0-1_swift-label>Swift</label><div class=code-tabpanel role=tabpanel data-lang=swift id=tab-group-0-1_swift-panel aria-labelledby=tab-group-0-1_swift-label><pre><code class=swift>fileprivate var firstHMILevel: SDLHMILevel = .none
func hmiLevel(_ oldLevel: SDLHMILevel, didChangeToLevel newLevel: SDLHMILevel) {
}
</code></pre></div></div>

<div class=md-fenced-code-tabs id=tab-tab-group-1><input name=tab-group-1 type=radio id=tab-group-1-0_objc checked=checked class=code-tab data-lang=objc aria-controls=tab-group-1-0_objc-panel role=tab><label for=tab-group-1-0_objc class=code-tab-label data-lang=objc id=tab-group-1-0_objc-label>Objc</label><div class=code-tabpanel role=tabpanel data-lang=objc id=tab-group-1-0_objc-panel aria-labelledby=tab-group-1-0_objc-label><pre><code class=objc>- (void)hmiLevel:(SDLHMILevel)oldLevel didChangeToLevel:(SDLHMILevel)newLevel {
}
</code></pre></div><input name=tab-group-1 type=radio id=tab-group-1-1_swift class=code-tab data-lang=swift aria-controls=tab-group-1-1_swift-panel role=tab><label for=tab-group-1-1_swift class=code-tab-label data-lang=swift id=tab-group-1-1_swift-label>Swift</label><div class=code-tabpanel role=tabpanel data-lang=swift id=tab-group-1-1_swift-panel aria-labelledby=tab-group-1-1_swift-label><pre><code class=swift>fileprivate var firstHMILevel: SDLHMILevel = .none
func hmiLevel(_ oldLevel: SDLHMILevel, didChangeToLevel newLevel: SDLHMILevel) {
}
</code></pre></div></div>"""

        html = markdown.markdown(
            text,
            extensions=self.MARKDOWN_EXTENSIONS,
            output_format='html5')

        self.maxDiff = len(html) * 2
        self.assertEqual(html, expected_output)

