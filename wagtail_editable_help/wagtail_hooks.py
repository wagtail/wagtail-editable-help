from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import HelpTextString, populate_help_text_strings


_has_populated_records = False


class HelpTextAdmin(ModelAdmin):
    model = HelpTextString
    menu_label = "Help text"
    menu_icon = "help"
    add_to_settings_menu = True
    list_display = ('identifier', 'text')

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
