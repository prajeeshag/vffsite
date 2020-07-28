from random import randint

from django.template import Template
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from crispy_forms.layout import (Div, Field, LayoutObject, TemplateNameMixin)
from crispy_forms.utils import TEMPLATE_PACK, flatatt, render_field


class PrependedAppendedAny(Field):
    template = "prepended_appended_any.html"

    def __init__(self, field, prepended_text=None, appended_text=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if "active" in kwargs:
            self.active = kwargs.pop("active")

        self.input_size = None
        css_class = kwargs.get("css_class", "")
        if "input-lg" in css_class:
            self.input_size = "input-lg"
        if "input-sm" in css_class:
            self.input_size = "input-sm"

        super().__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        extra_context = extra_context.copy() if extra_context is not None else {}
        extra_context.update(
            {
                "crispy_appended_text": self.appended_text,
                "crispy_prepended_text": self.prepended_text,
                "input_size": self.input_size,
                "active": getattr(self, "active", False),
            }
        )
        if hasattr(self, "wrapper_class"):
            extra_context["wrapper_class"] = self.wrapper_class
        template = self.get_template_name(template_pack)
        return render_field(
            self.field,
            form,
            form_style,
            context,
            template=template,
            attrs=self.attrs,
            template_pack=template_pack,
            extra_context=extra_context,
            **kwargs,
        )
