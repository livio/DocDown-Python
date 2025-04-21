import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from .docdown import TemplateRenderMixin

DEFAULT_ADAPTER = "docdown.template_adapters.StringFormatAdapter"


class SequenceDiagramBlockPreprocessor(TemplateRenderMixin, Preprocessor):
    RE = re.compile(
        r"^\s*\|{3,}\s*?\n(?P<content>[\s\S\n]*?)!(\[(?P<title>.*)\])?\((?P<url>\S*)\)\n\|{3,}", re.MULTILINE
    )

    def __init__(self, media_url=None, prefix="", postfix="", template_adapter=DEFAULT_ADAPTER, **kwargs):
        self.media_url = media_url
        self.prefix = prefix
        self.postfix = postfix
        self.template_adapter = template_adapter
        super().__init__(template_adapter=template_adapter, **kwargs)

    def run(self, lines):
        text = "\n".join(lines)
        renderer = self.get_template_adapter()

        while 1:
            m = self.RE.search(text)
            if m:
                content = m.group("content")
                image_url = m.group("url")
                title = m.group("title") or "Sequence Diagram"

                if image_url.startswith("./"):
                    image_url = image_url[2:]  # ./assets/image.png -> assets/image.png

                if self.media_url is not None:
                    if not image_url.lower().startswith("http") and not image_url.startswith("//"):
                        image_url = self.media_url + image_url

                context = {"image_url": image_url, "title": title}

                prefix = renderer.render(template=self.prefix, context=context)
                postfix = renderer.render(template=self.postfix, context=context)

                start_tag = self.md.htmlStash.store(prefix)
                end_tag = self.md.htmlStash.store(postfix)

                text = "{}\n{}\n\n{}\n{}\n{}".format(text[: m.start()], start_tag, content, end_tag, text[m.end() :])
            else:
                break

        return text.split("\n")


class SequenceDiagramExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "prefix": ["<div>", "Opening tag(s) which wrap the content"],
            "postfix": ["</div>", "Closing tag(s) which wrap the content"],
            "media_url": [".", "Path to the media"],
            "template_adapter": [
                "docdown.template_adapters.StringFormatAdapter",
                ("Adapter for rendering prefix and postfix templates using your template language of choice."),
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """Add SequenceDiagramBlockPreprocessor to the Markdown instance."""
        md.registerExtension(self)

        media_url = self.getConfig("media_url")
        prefix = self.getConfig("prefix")
        postfix = self.getConfig("postfix")
        template_adapter = self.getConfig("template_adapter")

        md.preprocessors.register(
            SequenceDiagramBlockPreprocessor(
                media_url=media_url,
                prefix=prefix,
                postfix=postfix,
                template_adapter=template_adapter,
                md=md,
            ),
            "sequence",
            29,  # after normalize_whitespace
        )


def makeExtension(*args, **kwargs):
    return SequenceDiagramExtension(*args, **kwargs)
