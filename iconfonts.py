"""
IconFonts Extension for Python-Markdown
========================================

Version: 1.0

Description:
	Use this extension to display icon font icons in python markdown. Just add the css necessary for your font and add this extension.

Features:
	- Support FontAwesome or Bootstrap/Glyphicons or both at the same time!
	- Allow users to specify additional modifiers, like 'fa-2x' from FontAwesome
	- Force users to use pre-defined classes to style their icons instead of
		allowing them to specify styles themselves
	- Allow users to specify additional classes, like 'red'

Syntax:
	- Accepts a-z, A-Z, 0-9, _ (underscore), and - (hypen)
	- Uses HTML Entity like syntax

	&icon-html5;
	&icon-css3;
	&icon-my-icon;

	&icon-html5:2x;
	&icon-quote:3x,muted;
	&icon-spinner:large,spin;


Example Markdown:
	I love &icon-html5; and &icon-css3;
	&icon-spinner:large,spin; Sorry we have to load...
	&icon-spinner:large,spin:red; Sorry we have to load...

Output:
	I love <i aria-hidden="true" class="icon-html5"></i> and <i aria-hidden="true" class="icon-css3"></i>
	<i aria-hidden="true" class="icon-spinner icon-large icon-spin"></i> Sorry we have to load...
	<i aria-hidden="true" class="icon-spinner icon-large icon-spin red"></i> Sorry we have to load...


Installation:
	Just drop it in the extensions folder of the markdown package. (markdown/extensions).
	Also check out: https://pythonhosted.org/Markdown/extensions/index.html

Usage/Setup:
	Default Prefix is "icon-":
		In a Django Template:
			{{ textmd|markdown:"safe,iconfonts" }}

		In Python:
			>>> text = '&icon-html5;'
			>>> md = markdown.Markdown(extensions=['iconfonts'])
			>>> converted_text = md.convert(text)
			'<i aria-hidden="true" class="icon-html5"></i>'


	Using a custom Prefix:
		In a Django Template:
			{{ textmd|markdown:"safe,iconfonts(prefix=mypref-)" }}

		In Python:
			>>> text = '&mypref-html5;'
			>>> md = markdown.Markdown(extensions=['iconfonts(prefix=mypref-)'])
			>>> converted_text = md.convert(text)
			'<i aria-hidden="true" class="mypref-html5"></i>'


	Using no prefix:
		In a Django Template:
			{{ textmd|markdown:"safe,iconfonts(prefix=)" }}

		In Python:
			>>> text = '&html5;'
			>>> md = markdown.Markdown(extensions=['iconfonts(prefix=)'])
			>>> converted_text = md.convert(text)
			'<i aria-hidden="true" class="html5"></i>'

	Use the base option which allows for Bootstrap 3 and FontAwesome 4:
		In Python:
			>>> text = '&fa-html5;'
			>>> md = markdown.Markdown(extensions=['iconfonts(prefix=fa-, base=fa)'])
			>>> converted_text = md.convert(text)
			'<i aria-hidden="true" class="fa icon-html5"></i>'

			>>> text = '&glyphicon-remove;'
			>>> md = markdown.Markdown(extensions=['iconfonts(prefix=glyphicon-, base=glyphicon)'])
			>>> converted_text = md.convert(text)
			'<i aria-hidden="true" class="glyphicon glyphicon-remove"></i>'

	Or support both Bootstrap 3/Glyphicons and FontAwesome 4 at the same time:
		In Python:
			>>> text = '&fa-html5; &glyphicon-remove;''
			>>> md = markdown.Markdown(extensions=['iconfonts'],
			>>>                        extension_configs={
			>>>                            'fa': 'fa',
			>>>                            'glyphicon': 'glyphicon',
			>>>                        })
			>>> converted_text = md.convert(text)
			'<i aria-hidden="true" class="fa fa-html5"></i>'
			'<i aria-hidden="true" class="glyphicon glyphicon-remove"></i>'


Copyright 2014 [Eric Eastwood](http://ericeastwood.com/)
          2024 [Tom Hubrecht](https://hubrecht.ovh)
"""

__VERSION__ = "4.0"

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


def makeExtension(**kwargs):
    return IconFontsExtension(**kwargs)
