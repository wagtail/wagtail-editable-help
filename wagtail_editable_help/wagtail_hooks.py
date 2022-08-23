from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import HelpTextString


class HelpTextAdmin(ModelAdmin):
    model = HelpTextString
    menu_label = "Help text"
    menu_icon = "help"
    add_to_settings_menu = True
    list_display = ('identifier', 'text')


modeladmin_register(HelpTextAdmin)
