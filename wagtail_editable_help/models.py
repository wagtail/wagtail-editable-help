from django.db import models
from django.utils.deconstruct import deconstructible


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
