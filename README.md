# HtmlToHaml
This script converts HTML code to HAML (for django-hamlpy).
If you use django-hamlpy (https://github.com/nyaruka/django-hamlpy) as a template renderer for your django project
you might find it hard to convert existing HTML code to HAML. Django-hamlpys HAML syntax is a little different from
other HAML syntaxes so existing online converters won't work. <br>
This script does work tho :)

# Installation
Just clone this repo. No other dependencies required. The Script was developed and tested on Python 3.9.

# Converting files
The script takes two important parameters `input` (required), the path to the input file and 
`--output` (optional) the output path. If `--output` is not set, the `input` filename
with the `.haml` file extension will be used as the output file name. <br>
Take a look at the script for more parameters

## Examples
### Example usage 1

``
HamlConverter.py index.html
``
<br> Will save the result to `index.haml`

### Example usage 2

``
HamlConverter.py index.html --output output.asdf
``
<br> Will save the result to `output.asdf`

# Link handlers
Django has its own template language to render links and static files (https://docs.djangoproject.com/en/3.1/intro/tutorial06/)
You can overwrite the following methods to patch links `patch_link_links, patch_a_links, patch_script_links and patch_img_links`
These methods take the link as input (eg. "/js/example.js" or "http://example.com/script.js") and return the patched script link.
The default conversion for the first example would convert it to `{% static '/js/example.js' %}`

You probably want to overwrite these methods to make them work for your use case.

# Improvements
The Script was tested on a "large" website and worked quite well. If you encounter a problem,
feel free to submit a pull request.

