import re
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import LINK_RE, LinkInlineProcessor


class DocDownLinkInlineProcessor(LinkInlineProcessor):
    def __init__(self, link_map=None, *args, **kwargs):
        self.link_map = link_map or {}
        super().__init__(*args, **kwargs)

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:  # type: ignore
        """Return an `a` [`Element`][xml.etree.ElementTree.Element] or `(None, None, None)`."""
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        href = self.link_map_url(href)

        el = etree.Element("a")
        el.text = text

        el.set("href", href)

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index

    def link_map_url(self, url):
        if "#" in url:
            uri, uri_hash = url.split("#", 1)
        else:
            uri = url
            uri_hash = ""

        if uri in self.link_map:
            uri = self.link_map.get(uri)

        if uri_hash:
            uri = "{}#{}".format(uri, uri_hash)

        return uri


class LinksExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "link_map": [{}, "Dict mapping source urls to target urls."],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        link_map = self.getConfig("link_map")
        # unregister the default links inline processor
        md.inlinePatterns.deregister("link", strict=True)
        # register the DocDown links inline processor
        md.inlinePatterns.register(DocDownLinkInlineProcessor(link_map=link_map, pattern=LINK_RE, md=md), "link", 160)


def makeExtension(*args, **kwargs):
    return LinksExtension(*args, **kwargs)
