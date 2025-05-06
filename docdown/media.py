from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class MediaTreeprocessor(Treeprocessor):
    def __init__(self, media_url=None, *args, **kwargs):
        self.media_url = media_url
        super().__init__(*args, **kwargs)

    def run(self, root):
        if self.media_url is not None:
            image_tags = root.findall(".//img")
            for image_tag in image_tags:
                tag_src = image_tag.get("src")
                if not tag_src.lower().startswith("http") and not tag_src.startswith("//"):
                    if tag_src.startswith("./"):
                        tag_src = tag_src[2:]
                    # TODO: relative image tag source starting with . like sequence
                    # diagrams?

                    # Make sure we don't create a url like http://example.org//something.html
                    # if media_url ends with / and tag_src starts with /
                    # example.com/ + /blah.html = example.com/blah.html
                    # example.com + /blah.html = example.com/blah.html
                    # example.com/ + blah.html = example.com/blah.html
                    # example.com + blah.html = example.com/blah.html
                    # example.com + ./blah.html = example.com/blah.html
                    image_tag.set("src", self.media_url.rstrip("/") + "/" + tag_src.lstrip("/"))


class MediaExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "media_url": [".", "Path or URL base for the media"],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Add MediaTreeprocessor to the Markdown instance."""
        md.registerExtension(self)

        media_url = self.getConfig("media_url")
        md.treeprocessors.register(
            MediaTreeprocessor(media_url=media_url, md=md),
            "media",
            19,  # after inline tree preprocessor
        )


def makeExtension(*args, **kwargs):
    return MediaExtension(*args, **kwargs)
