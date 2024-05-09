import re
import xml.etree.ElementTree as etree
from collections import defaultdict

from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


class IconFontsPattern(InlineProcessor):
    """
    Return an <i> element with the necessary classes
    """

    _base: str
    _prefix: str

    def __init__(self, pattern: str, md: Markdown, base: str = "", prefix: str = ""):
        super().__init__(pattern, md)

        self._base = base
        self._prefix = prefix

    def handleMatch(self, m: re.Match, data: str):
        # The dictionary keys come from named capture groups in the regex
        match_dict = m.groupdict()

        el = etree.Element("i")

        name = match_dict["name"]

        classes: dict[str, str] = defaultdict(str)

        if self._base:
            classes["base"] = self._base

        classes["name"] = f"{self._prefix}{name}"

        # Mods are modifier classes. The syntax in the markdown is:
        # "&icon-namehere:2x;" and with multiple "&icon-spinner:2x,spin;"

        if match_dict["mod"] is not None:
            # Make a string with each modifier like: "fa-2x fa-spin"
            classes["mod"] = " ".join(
                map(
                    lambda c: self._prefix + c,
                    filter(None, match_dict["mod"].split(",")),
                )
            )

        # User mods are modifier classes that shouldn't be prefixed with
        # prefix. The syntax in the markdown is:
        # "&icon-namehere::red;" and with multiple "&icon-spinner::red,bold;"
        if match_dict["user_mod"] is not None:
            # Make a string with each modifier like "red bold"
            classes["user_mod"] = " ".join(
                filter(None, match_dict["user_mod"].split(","))
            )

        el.set("class", " ".join(classes.values()))

        # This is for accessibility and text-to-speech browsers
        # so they don't try to read it
        el.set("aria-hidden", "true")

        return el, m.start(0), m.end(0)


ICON_RE = r"(?P<name>[a-zA-Z0-9-]+)(:(?P<mod>[a-zA-Z0-9-]+(,[a-zA-Z0-9-]+)*)?(:(?P<user_mod>[a-zA-Z0-9-]+(,[a-zA-Z0-9-]+)*)?)?)?;"
#           ^---------------------^^ ^                    ^--------------^ ^ ^ ^                         ^--------------^ ^ ^ ^
#                                  | +-------------------------------------+ | +------------------------------------------+ | |
#                                  |                                         +----------------------------------------------+ |
#                                  +------------------------------------------------------------------------------------------+


class IconFontsExtension(Extension):
    """IconFonts Extension for Python-Markdown."""

    def __init__(self, **kwargs):

        self.config = {
            "prefix": ["icon-", "Custom class prefix."],
            "base": ["", "Base class added to each icon"],
            "prefix_base_pairs": [{}, "Prefix/base pairs"],
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown):
        # Register the global pattern
        md.inlinePatterns.register(
            IconFontsPattern(
                f"&{self.getConfig('prefix')}{ICON_RE}",
                md,
                base=self.getConfig("base"),
                prefix=self.getConfig("prefix"),
            ),
            "iconfonts",
            175,
        )

        # Register each of the pairings
        for prefix, base in self.getConfig("prefix_base_pairs").items():
            md.inlinePatterns.register(
                IconFontsPattern(f"&{prefix}{ICON_RE}", md, base=base, prefix=prefix),
                f"iconfonts_{prefix.rstrip('-')}",
                175,
            )
