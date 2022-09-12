from django.db import models
try:
    from wagtail.models import Page
except ImportError:
    from wagtail.core.models import Page

try:
    from wagtail.admin.panels import FieldPanel
except ImportError:
    from wagtail.admin.edit_handlers import FieldPanel

from wagtail_editable_help.models import HelpText


class HomePage(Page):
    tagline = models.CharField(max_length=255, help_text=HelpText("Home page", "tagline", default="Write something snappy here"))
    body = models.TextField(blank=True, help_text=HelpText("Home page", "body"))

    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
        FieldPanel("body"),
    ]
