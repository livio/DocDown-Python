######################
Scoped Code Tabs
######################

Scoped Code Tabs allows for the explicit annotation of when and where to tabulate a set of code blocks versus rendering them
separately.

A scoped code tab is delimited by an opening ``|~`` fence and closing ``~|`` fence. The code blocks within the fences
are defined as typical code blocks, using backticks, with the opening backtick fence specifying the code language contained
within the block.

The configuration for rendering the tabs is as directly defined by the `fenced_code_tabs` extension.

==============
Configuration
==============

single_block_as_tab
    Whether a single code block should still be rendered as a code tab. Default: ``False``
active_class
    The CSS class to apply to the active tab. Default: ``active``
template
    Which template to use to render code tabs. One of: [``default``, ``bootstrap3``, ``bootstrap4``, ``bootstrap5``]. Default: ``default``
    Please see the *-template.html files in the `fenced_code_tabs` extension.


=======
Usage
=======
In documents
-------------

.. code-block:: md

    ### Hello World Examples
    |~
    ```bash
    helloWorld() {
    greeting=${1:-World}
    echo(`Hello ${greeting}`)
    }
    ```
    ~|

    ```python
    def hello_world(greeting: str = "World") -> None:
    print(f"Hello {greeting}")
    ```

Python
--------------

.. code-block:: python

    config = {
        'docdown.scoped_code_tabs': {
            'single_block_as_tab': True,
            'template': 'bootstrap4',
            'active_class': 'tab-active'
        }
    }

    text = """\
    ### Hello World Examples
    |~
    ```bash
    helloWorld() {
    greeting=${1:-World}
    echo(`Hello ${greeting}`)
    }
    ```
    ~|
    ```python
    def hello_world(greeting: str = "World") -> None:
    print(f"Hello {greeting}")
    ```
    """

    html = markdown.markdown(
        text,
        extensions=['docdown.scoped_code_tabs'],
        extension_configs=config,
        output_format='html5')

=======
Output
=======
Note the extra classes and divs for tabulation around the ``|~`` ``~|`` code block.

.. code-block:: html

   <h3>Hello World Examples</h3>
    <p> <div class=md-fenced-code-tabs id=tab-tab-group-0><ul class="nav nav-tabs"><li class=nav-item><a class="nav-link tab-active" href=#tab-group-0-0_bash-panel role=tab id=tab-group-0-0_bash-tab data-toggle=tab data-lang=bash aria-controls=tab-group-0-0_bash-panel aria-selected=true>Bash</a></li></ul><div class=tab-content><div id=tab-group-0-0_bash-panel class="tab-pane show tab-active" role=tabpanel aria-labelledby=tab-group-0-0_bash-tab><pre><code class=bash>helloWorld() {
    greeting=${1:-World}
    echo(`Hello ${greeting}`)
    }
    </code></pre></div></div></div></p>
    <p><code>python
    def hello_world(greeting: str = "World") -&gt; None:
    print(f"Hello {greeting}")</code></p>

.. _`markdown_fenced_code_tabs`: https://github.com/yacir/markdown-fenced-code-tabs
