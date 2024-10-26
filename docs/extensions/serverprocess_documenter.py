"""
A modified version of https://github.com/jupyterhub/autodoc-traits/tree/1.2.2
for documenting trait fields that are used to configure another object, but
where the traitlet cannot be set directly.

This is used to generate the Server Process options documentation:
https://github.com/jupyterhub/jupyter-server-proxy/blob/main/docs/source/server-process.md
"""

from sphinx.application import Sphinx
from sphinx.ext.autodoc import (
    SUPPRESS,
    AttributeDocumenter,
    ClassDocumenter,
    ObjectMember,
)
from sphinx.util.typing import ExtensionMetadata
from traitlets import MetaHasTraits, TraitType, Undefined


class ServerProcessConfigurableDocumenter(ClassDocumenter):
    """
    A modified version of autodoc_traits.ConfigurableDocumenter that only documents
    the traits in this class, not the inherited traits.
    https://github.com/jupyterhub/autodoc-traits/blob/1.2.2/autodoc_traits.py#L20-L122
    """

    objtype = "serverprocessconfigurable"
    directivetype = "class"
    priority = 100  # higher priority than ClassDocumenter's 10

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, MetaHasTraits)

    def get_object_members(self, want_all):
        """
        Only document members in this class
        """
        config_trait_members = self.object.class_traits(config=True).items()
        members = [ObjectMember(name, trait) for (name, trait) in config_trait_members]
        return False, members

    def should_suppress_directive_header():
        return True

    def add_directive_header(self, sig):
        print(f"{sig=}")
        self.options.annotation = SUPPRESS
        super().add_directive_header(sig)


class ServerProcessTraitDocumenter(AttributeDocumenter):
    """
    A modified version of autodoc_traits.TraitDocumenter that omits the c.ClassName prefix
    https://github.com/jupyterhub/autodoc-traits/blob/1.2.2/autodoc_traits.py#L125-L203
    """

    objtype = "serverprocesstrait"
    directivetype = "attribute"
    priority = 100  # AttributeDocumenter has 10
    member_order = 0  # AttributeDocumenter has 60

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, TraitType)

    def add_directive_header(self, sig):
        default_value = self.object.default_value
        if default_value is Undefined:
            default_value = ""
        else:
            default_value = repr(default_value)

        traitlets_type = self.object.__class__.__name__
        self.options.annotation = f"{traitlets_type}({default_value})"
        super().add_directive_header(sig)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.setup_extension("sphinx.ext.autodoc")
    app.add_autodocumenter(ServerProcessConfigurableDocumenter)
    app.add_autodocumenter(ServerProcessTraitDocumenter)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
