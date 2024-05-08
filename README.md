# markdown-icons (`iconfonts.py`)

Easily display icon fonts in python markdown. Just add the CSS necessary for your font and add this extension.

This is a 3rd party extension for [Python Markdown](https://pythonhosted.org/Markdown/). You can see a [full list of 3rd party extensions here](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions).

Although this works with any icon font, users can use a `mod` syntax to add more prefixed classes to support [Font Awesome](https://fontawesome.com/) and its special classes such as `2x, 3x, muted, spin, etc`

Furthermore, users can add their own `user_mod` syntax to add additional, non-prefixed, pre-defined classes for greater control over their icons while allowing you to control exactly what styles are allowed.

See the [python markdown documentation](https://python-markdown.github.io/) for more information.

# Current Version: 3.0

# Syntax:

- Accepts a-z, A-Z, 0-9, \_(underscore), and - (hypen)
- Uses [HTML Entity](http://www.w3schools.com/html/html_entities.asp) like syntax: `&entity_name;`

```
&icon-html5;
&icon-css3;
&icon-my-icon;
```

Mod syntax:

```
&icon-html5:2x;
&icon-quote:3x,muted;
&icon-spinner:large,spin;
```

User mod syntax:

```
&icon-html5::red;
&icon-quote:2x:bold;
```

#### Example Markdown:

```
I love &icon-html5; and &icon-css3;
&icon-spinner:large,spin; Sorry we have to load...
```

##### Output:

```
I love <i aria-hidden="true" class="icon-html5"></i> and <i aria-hidden="true" class="icon-css3"></i>
<i aria-hidden="true" class="icon-spinner icon-large icon-spin"></i> Sorry we have to load...
```

# Usage / Setup:

#### Default Prefix is "icon-":

```python
md = markdown.Markdown(extensions=["iconfonts"])
converted_text = md.convert(text)
```

#### Use a custom Prefix:

```python
md = markdown.Markdown(
    extensions=["iconfonts"],
    extension_configs={"iconfonts": {"prefix": "mypref-"}},
)
converted_text = md.convert(text)
```

#### No prefix:

This isn't suggested, as it will take over the already built in HTML Entities

```python
md = markdown.Markdown(
    extensions=["iconfonts"],
    extension_configs={"iconfonts": {"prefix": ""}},
)
converted_text = md.convert(text)
```

#### The `base` option allows for use of Bootstrap and FontAwesome icons

```python
md = markdown.Markdown(extensions=['iconfonts'])
converted_text = md.convert(text)
```

**Input:** `&icon-html5;`

**Output:** `<i aria-hidden="true" class="icon icon-html5"></i>`

#### Combine options with a comma:

```python
md = markdown.Markdown(
    extensions=["iconfonts"],
    extension_configs={"iconfonts": {"prefix": "fa-", "base": "fa"}},
)
converted_text = md.convert(text)
```

**Input!** `&icon-spinner:spin:red,bold;`

**Output:** `<i aria-hidden="true" class="icon-spinner icon-spin red bold"></i>`

#### `prefix_base_pairs` option

The `prefix_base_pairs` option allows for multiple prefix-base pairs to be specified, to allow you to support both Bootstrap 3/Glyphicon and FontAwesome icons

```python
md = markdown.Markdown(extensions=['iconfonts'],
                       extension_configs={
                           'iconfonts': {
                               'prefix_base_pairs': {
                                   'fa-': 'fa',
                                   'glyphicon-': 'glyphicon',
                               }
                           }
                       })
converted_text = md.convert(text)
```

**Input:** `&glyphicon-remove; &fa-html5;`

**Output:** `<i aria-hidden="true" class="glyphicon glyphicon-remove"></i> <i aria-hidden="true" class="fa fa-html5"></i>`
