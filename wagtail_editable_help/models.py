from django.db import models
from django.utils.deconstruct import deconstructible


class HelpTextString(models.Model):
    identifier = models.CharField(max_length=255, unique=True, editable=False, db_index=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return "<HelpText: %s=%r>" % (self.identifier, self.text)

    class Meta:
        ordering = ("identifier",)


_help_text_objects = set()


@deconstructible
class HelpText:
    def __init__(self, identifier, default=""):
        self.identifier = identifier
        self.default = default
        _help_text_objects.add(self)

    def __str__(self):
        str, created = HelpTextString.objects.get_or_create(
            identifier=self.identifier, defaults={'text': self.default}
        )
        return str.text

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return isinstance(other, HelpText) and other.identifier == self.identifier


def populate_help_text_strings():
    """
    Ensure that a HelpTextString record exists in the database for all HelpText
    definitions that have been encountered during module loading
    """
    for item in _help_text_objects:
        str(item)
