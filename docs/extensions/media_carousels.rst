######################
Media Carousels
######################
Media Carousels meets a very specific use case wherein a list of images are wrapped in outer HTML and given class attributes
that allow them to be styled to achieve a carousel effect.


=============
Dependencies
=============
There are no required dependencies.

==============
Configuration
==============
There are no configuration options at this time.


=======
Usage
=======
In documents
-------------

.. code-block:: md

    [carousel!]
    ![image alt 1](/path/to/img1.jpg "image 1")
    ![image alt 2](/path/to/img2.jpg "image 2")
    ![image alt 3](/path/to/img3.jpg "image 3")
    [!carousel]

Python
--------------

.. code-block:: python


    text = """\
    [carousel!]
    ![image alt 1](/path/to/img1.jpg "image 1")
    ![image alt 2](/path/to/img2.jpg "image 2")
    ![image alt 3](/path/to/img3.jpg "image 3")
    [!carousel]
    """

    html = markdown.markdown(
        text,
        extensions=['docdown.media_carousels'],
        extension_configs=config,
        output_format='html5')

=======
Output
=======
.. code-block:: html

    <div class="carousel-container">
    <div class="vanilla-zoom" id="docs-gallery">
    <div class="carousel-sidebar">
    <img class="small-preview" src="/path/to/img1.jpg" alt="image alt 1" title="image 1">
    <img class="small-preview" src="/path/to/img2.jpg" alt="image alt 2" title="image 2">
    </div>
    <div class="zoomed-desc">
    <div class="zoomed-image"></div>
    <p class="zoomed-text"></p>
    </div>
    </div>
    </div>
