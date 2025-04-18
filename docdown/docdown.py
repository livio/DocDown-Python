import importlib


class TemplateRenderMixin:
    """
    Mixin for extensions which render templates as part of their output
    """

    def __init__(self, template_adapter="", *args, **kwargs):
        self.template_adapter = template_adapter
        super().__init__(*args, **kwargs)

    def get_template_adapter(self):
        module_name, class_name = self.template_adapter.rsplit(".", 1)
        my_module = importlib.import_module(module_name)
        AdapterClass = getattr(my_module, class_name)
        return AdapterClass()
