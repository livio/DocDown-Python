from markdown.extensions import Extension
from markdown.inlinepatterns import LINK_RE, LinkInlineProcessor


class DocDownLinkInlineProcessor(LinkInlineProcessor):
    def __init__(self, link_map=None, **kwargs):
        self.link_map = link_map or {}
        super().__init__(**kwargs)

    def sanitize_url(self, url):
        if "#" in url:
            uri, uri_hash = url.split("#", 1)
        else:
            uri = url
            uri_hash = ""

        if uri in self.link_map:
            uri = self.link_map.get(uri)

        if uri_hash:
            uri = "{}#{}".format(uri, uri_hash)
        return super().sanitize_url(uri)


class LinksExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "link_map": [{}, "Dict mapping source urls to target urls."],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        link_map = self.getConfig("link_map")
        # unregister the default links inline processor
        md.inlinePatterns.deregister("links", strict=False)
        # register the DocDown links inline processor
        md.inlinePatterns.register(DocDownLinkInlineProcessor(link_map=link_map, pattern=LINK_RE, md=md), "links", 160)


def makeExtension(*args, **kwargs):
    return LinksExtension(*args, **kwargs)
