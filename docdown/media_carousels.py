# -*- coding: utf-8 -*-

"""
media_carousels
----------------------------------

docdown.media_carousels Markdown extension module
"""
from __future__ import absolute_import, unicode_literals, print_function

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor

BEFORE_CAROUSEL_HTML = """<div class="carousel-container">
<div class="vanilla-zoom" id="docs-gallery-{}">
<div class="carousel-sidebar">"""

AFTER_CAROUSEL_HTML = """</div>
<div class="zoomed-desc">
<div class="zoomed-image"></div>
<p class="zoomed-text"></p>
</div>
</div>
</div>"""

class MediaCarouselPostprocessor(Postprocessor):
    """
    Replaces the [carousel!] ... [!carousel] fences with the correct
        outer HTML, and adds the small-preview class to its images.
    """

    def run(self, text):
        """
        At this point the carousel markdown should look like
        <p>[carousel!]
        <img src="...">
        <img src="...">
        <img src="...">
        [!carousel]</p>

        =======
        What we need is
        <div class="carousel-container">
            <div class="vanilla-zoom" id="docs-gallery-0">
                <div class="carousel-sidebar">
                    <img class="small-preview" src="...">
                    <img class="small-preview" src="...">
                    <img class="small-preview" src="...">
                </div>
                <div class="zoomed-desc">
                    <div class="zoomed-image"></div>
                    <p class="zoomed-text"></p>
                </div>
            </div>
        </div>
        """
        CAROUSEL_START = "[carousel!]"
        CAROUSEL_END = "[!carousel]"
        split_text = text.split(CAROUSEL_START, maxsplit=1)

        result_text = ''

        counter = 0
        while len(split_text) == 2:
            before_carousel, carousel_start = split_text

            # Remove any added wrapper paragraph tags, only if closing carousel present
            if CAROUSEL_END in carousel_start and before_carousel.endswith('<p>'):
                before_carousel = before_carousel[:len(before_carousel) - 3]
            # Add before carousel to result
            result_text += before_carousel

            # Process carousel
            split_carousel = carousel_start.split(CAROUSEL_END, maxsplit=1)
            if len(split_carousel) == 2:
                # process carousel content
                carousel = split_carousel[0]

                # Add opening divs
                result_text += BEFORE_CAROUSEL_HTML.format(counter)
                counter += 1

                # Find all img tags
                images = carousel.split('<img ')
                result_text += images[0]
                for img in images[1:]:
                    new_text = ''
                    if 'class="' in img:
                        # Already has a class, make small-preview the first
                        new_text = img.replace('class="', 'class="small-preview ')
                    elif img:
                        # no class attribute -> add it
                        new_text = 'class="small-preview" ' + img
                    result_text += "<img " + new_text

                # Add closing divs and description text
                result_text += AFTER_CAROUSEL_HTML

            # Remove any added wrapper paragraph tags
            if split_carousel[-1].startswith('</p>'):
                split_carousel[-1] = split_carousel[-1][4:]

            # split the last element in the result of splitting on CAROUSEL_END to update split_text
            split_text = split_carousel[-1].split(CAROUSEL_START, maxsplit=1)

        result_text += split_text[-1]
        return result_text


class MediaCarouselExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add MediaCarouselPostprocessor to the Markdown instance. """
        md.registerExtension(self)
        md.postprocessors.add('media_carousels',
                             MediaCarouselPostprocessor(md), '>amp_substitute')


def makeExtension(*args, **kwargs):
    return MediaCarouselExtension(*args, **kwargs)
