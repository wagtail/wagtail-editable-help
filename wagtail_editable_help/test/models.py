from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_editable_help.models import HelpText


class HomePage(Page):
    tagline = models.CharField(max_length=255, help_text=HelpText("Home page", "tagline", default="Write something snappy here"))
    body = models.TextField(blank=True, help_text=HelpText("Home page", "body"))
    sidebar = StreamField([
        ("link", blocks.PageChooserBlock(help_text=HelpText("Home page", "sidebar link", default="Choose up to 5 links")))
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
        FieldPanel("body"),
        FieldPanel("sidebar"),
    ]
