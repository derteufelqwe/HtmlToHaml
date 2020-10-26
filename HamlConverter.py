from html.parser import HTMLParser
from argparse import ArgumentParser

INDENT = 2

NO_INDENT = ['link', 'meta', 'script', 'img', 'input']
TEXT_CHARS = [chr(i) for i in range(48, 91)]


class HtmlHamlParser(HTMLParser):

    def __init__(self, patchLinks=True):
        super().__init__()
        self._indent = 0
        self._data = self._setup_data()
        self._script_open = False
        self._patchLinks = patchLinks

    def _setup_data(self):
        return '- load static\n'

    @property
    def result(self):
        return self._data

    def handle_startendtag(self, tag, attrs):
        """
        Handles tags like <a ..../>
        """
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def _hnd_class_id(self, tag, attrs) -> str:
        """
        Special handling for id and class tags
        :return: HAML line
        """

        data = ''
        classes = [o[1] for o in attrs if o[0] == 'class']
        id = [o[1] for o in attrs if o[0] == 'id']

        if id:
            data += f'#{id[0]}'

        for class_group in classes:
            for clazz in class_group.split(' '):
                data += f'.{clazz}'

        return data

    def _hnd_attrs(self, tag, attrs) -> str:
        """
        Special handling for the attrs of a HTML line
        :return: HAML line
        """

        line = '{'
        for attr in attrs:
            key = attr[0]
            value = attr[1]
            if self._patchLinks:
                if tag == 'link' and key == 'href':
                    value = self.patch_link_links(value)
                elif tag == 'a' and key == 'href':
                    value = self.patch_a_links(value)
                elif tag == 'script' and key == 'src':
                    value = self.patch_script_links(value)
                elif tag == 'img' and key == 'src':
                    value = self.patch_script_links(value)

            if key in ('class', 'id'):
                continue

            if ' ' in key:
                line += f'"{key}": "{value}", '
            else:
                line += f'{key}: "{value}", '

        if line != '{':
            line = line[:-2]
            return f'{line}}}'

        return ''

    def handle_starttag(self, tag, attrs):
        self._data += f"{' ' * self._indent}%{tag}"

        if tag == 'script':
            self._script_open = True

        self._data += self._hnd_class_id(tag, attrs)

        if attrs:
            self._data += self._hnd_attrs(tag, attrs)

        self._data += '\n'
        if tag not in NO_INDENT:
            self._indent += INDENT

    def handle_endtag(self, tag):
        if tag not in NO_INDENT:
            self._indent -= INDENT

        if tag == 'script':
            self._script_open = False

    def handle_data(self, data):
        s = str(data).strip().strip('\n')
        script_open_indent = 0
        if self._script_open:
            script_open_indent = 2
        if s:
            if s[0] in TEXT_CHARS:
                self._data += f'{" " * (self._indent + script_open_indent)}{s}\n'
            else:
                self._data += f'{" " * (self._indent + script_open_indent)}"{s}"\n'

    def default_static_patch(self, link: str):
        if link.startswith('http'):
            return link

        return f"{{% static '{link}' %}}"

    def default_link_patch(self, link: str):
        return link

    def patch_link_links(self, link: str):
        return self.default_static_patch(link)

    def patch_a_links(self, link: str):
        return self.default_link_patch(link)

    def patch_script_links(self, link: str):
        return self.default_static_patch(link)

    def patch_img_links(self, link: str):
        return self.default_static_patch(link)

    def handle_comment(self, data):
        self._data += f'{" " * self._indent}<!-- {data} -->\n'


if __name__ == '__main__':
    description = """
    Converts HTML to HAML, which is valid for Djangos HAML template loader 'django-hamlpy'
    """

    parser = ArgumentParser(description=description)

    parser.add_argument('input', type=str, help='The input file (HTML).')
    parser.add_argument('--output', type=str, default=None, help='Optional name of the output file. Defaults to the name of the input file.')
    parser.add_argument('--patch-links', type=bool, default=True, help='Convert links to django template style.')

    args = parser.parse_args()
    inputFile = args.input
    if args.output != None:
        outputFile = args.output
    else:
        dotPos = args.input[::-1].find('.')
        if dotPos == -1:
            dotPos = None
        else:
            dotPos = -dotPos - 1
        outputFile = args.input[:dotPos] + '.haml'


    with open(inputFile, 'r') as file:
        htmlParser = HtmlHamlParser(patchLinks=args.patch_links)
        htmlParser.feed(file.read())

    with open(outputFile, 'w') as file:
        file.write(htmlParser.result)

    print(f'Converted {inputFile} to {outputFile}.')
