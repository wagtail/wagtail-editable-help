from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.html import format_html
from django.utils.translation import gettext as _
from telepath import StringAdapter
from wagtail.admin.admin_url_finder import AdminURLFinder

try:
    from wagtail.telepath import register
except ImportError:
    from wagtail.core.telepath import register

from .middleware import get_active_user


class HelpTextString(models.Model):
    model_label = models.CharField(max_length=255, editable=False)
    identifier = models.CharField(max_length=255, editable=False)
    text = models.TextField(blank=True)

    def __str__(self):
        return "%s - %s" % (self.identifier, self.model_label)

    def __repr__(self):
        return "<HelpText: %s %s=%r>" % (self.model_label, self.identifier, self.text)

    class Meta:
        ordering = ("model_label", "identifier",)
        constraints = [
            models.UniqueConstraint(fields=["model_label", "identifier"], name="unique_help_text_identifier"),
        ]
        indexes = [
            models.Index(fields=["model_label", "identifier"], name="help_text_identifier_idx")
        ]


_help_text_objects = set()


@deconstructible
class HelpText:
    def __init__(self, model_label, identifier, default=""):
        self.model_label = model_label
        self.identifier = identifier
        self.default = default
        _help_text_objects.add(self)

    def __str__(self):
        str, created = HelpTextString.objects.get_or_create(
            model_label=self.model_label, identifier=self.identifier,
            defaults={'text': self.default}
        )
        user = get_active_user()
        if user:
            finder = AdminURLFinder(user)
            edit_url = finder.get_edit_url(str)
        if user and edit_url:
            if str.text:
                return format_html('{} <a href="{}" class="edit-help-text">{}</a>', str.text, edit_url, _("Edit"))
            else:
                return format_html('<a href="{}" class="add-help-text">{}</a>', edit_url, _("Add help text"))
        else:
            return str.text

    def __hash__(self):
        return hash((self.model_label, self.identifier))

    def __eq__(self, other):
        return (
            isinstance(other, HelpText)
            and other.model_label == self.model_label
            and other.identifier == self.identifier
        )


def populate_help_text_strings():
    """
    Ensure that a HelpTextString record exists in the database for all HelpText
    definitions that have been encountered during module loading
    """
    for item in _help_text_objects:
        str(item)


class HelpTextAdapter(StringAdapter):
    def build_node(self, obj, context):
        return super().build_node(str(obj), context)


register(HelpTextAdapter(), HelpText)
