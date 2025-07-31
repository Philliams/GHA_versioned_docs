from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata

import json
import os



class HelloDirective(SphinxDirective):

    """A directive to say hello!"""


    required_arguments = 1


    def run(self) -> list[nodes.Node]:
            path = os.path.realpath(__file__)
            app = self.state.document.settings.env.app
            source_dir = app.srcdir
            filepath = self.arguments[0]

            full_path = os.path.join(source_dir, filepath)

            with open(full_path) as f:
                data = json.load(f)

                paragraph_node = nodes.paragraph(text=f'hello {data}!')

                return [paragraph_node]



def setup(app: Sphinx) -> ExtensionMetadata:

    app.add_directive('hello', HelloDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': False,
        'parallel_write_safe': False,
    }
