"""
A custom Sphinx directive to generate the Server Process options documentation:
https://github.com/jupyterhub/jupyter-server-proxy/blob/main/docs/source/server-process.md
"""

import importlib
from textwrap import dedent

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata
from traitlets import Undefined


class ServerProcessDirective(SphinxDirective):
    """A directive to say hello!"""

    required_arguments = 2

    def run(self) -> list[nodes.Node]:
        module = importlib.import_module(self.arguments[0], ".")
        cls = getattr(module, self.arguments[1])
        config_trait_members = cls.class_traits(config=True).items()

        doc = []

        for name, trait in config_trait_members:
            default_value = trait.default_value
            if default_value is Undefined:
                default_value = ""
            else:
                default_value = repr(default_value)
            traitlets_type = trait.__class__.__name__

            help = self.parse_text_to_nodes(dedent(trait.metadata.get("help", "")))

            definition = nodes.definition_list_item(
                "",
                nodes.term(
                    "",
                    "",
                    nodes.strong(text=f"{name}"),
                    nodes.emphasis(text=f" {traitlets_type}({default_value})"),
                ),
                nodes.definition("", *help),
            )
            doc.append(nodes.definition_list("", definition))
        return doc


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("serverprocess", ServerProcessDirective)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
