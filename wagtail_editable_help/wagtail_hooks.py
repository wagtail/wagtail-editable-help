from django.utils.html import format_html
from django.templatetags.static import static

try:
    from wagtail import hooks
except ImportError:
    from wagtail.core import hooks

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import HelpTextString, populate_help_text_strings


_has_populated_records = False


class HelpTextAdmin(ModelAdmin):
    model = HelpTextString
    menu_label = "Help text"
    menu_icon = "help"
    add_to_settings_menu = True
    list_display = ('identifier', 'model_label', 'text')
    search_fields = ('identifier', 'model_label', 'text')
    list_filter = ('model_label', )

    def get_queryset(self, request):
        # On first call to any ModelAdmin view that retrieves the queryset,
        # ensure that all HelpText definitions in the code have been turned into
        # HelpTextString records in the database
        global _has_populated_records
        if not _has_populated_records:
            populate_help_text_strings()
            _has_populated_records = True

        return super().get_queryset(request)


modeladmin_register(HelpTextAdmin)


@hooks.register("insert_global_admin_css")
def editable_help_css():
    return format_html('<link rel="stylesheet" href="{}">', static('wagtail_editable_help/wagtail_editable_help.css'))
