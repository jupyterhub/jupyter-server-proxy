from autodoc_traits import ConfigurableDocumenter, TraitDocumenter
from sphinx.application import Sphinx
from sphinx.ext.autodoc import SUPPRESS, ClassDocumenter, ObjectMember
from sphinx.util.typing import ExtensionMetadata
from traitlets import Undefined


class ServerProcessConfigurableDocumenter(ConfigurableDocumenter):
    objtype = "serverprocessconfigurable"
    directivetype = "class"
    priority = 100

    def get_object_members(self, want_all):
        """
        Only document members in this class
        """
        config_trait_members = self.object.class_traits(config=True).items()
        members = [ObjectMember(name, trait) for (name, trait) in config_trait_members]
        return False, members

    def should_suppress_directive_header():
        return True

    # Skip over autodoc_traits otherwise it'll prepend c.ServerProcess
    # to the annotation
    def add_directive_header(self, sig):
        print(f"{sig=}")
        self.options.annotation = SUPPRESS
        super(ClassDocumenter, self).add_directive_header(sig)


class ServerProcessTraitDocumenter(TraitDocumenter):
    objtype = "serverprocesstrait"
    directivetype = "attribute"
    priority = 100  # AttributeDocumenter has 10
    member_order = 0  # AttributeDocumenter has 60

    def add_directive_header(self, sig):
        default_value = self.object.default_value
        if default_value is Undefined:
            default_value = ""
        else:
            default_value = repr(default_value)

        traitlets_type = self.object.__class__.__name__
        self.options.annotation = f"{traitlets_type}({default_value})"
        # Skip over autodoc_traits otherwise it'll prepend c.ServerProcess
        # to the annotation
        super(TraitDocumenter, self).add_directive_header(sig)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.setup_extension("autodoc_traits")
    app.add_autodocumenter(ServerProcessConfigurableDocumenter)
    app.add_autodocumenter(ServerProcessTraitDocumenter)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
