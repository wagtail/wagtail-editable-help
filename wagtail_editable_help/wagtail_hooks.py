from django.utils.html import format_html
from django.templatetags.static import static

from wagtail import hooks
from wagtail import VERSION as WAGTAIL_VERSION

from .models import HelpTextString, populate_help_text_strings


_has_populated_records = False


if WAGTAIL_VERSION < (5, 2):
    from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

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

else:
    import django_filters
    from wagtail.snippets.models import register_snippet
    from wagtail.snippets.views.snippets import SnippetViewSet

    class HelpTextFilterSet(django_filters.FilterSet):
        model_label = django_filters.ChoiceFilter(choices=lambda: [
            (label, label)
            for label in HelpTextString.objects.values_list('model_label', flat=True).order_by('model_label').distinct()
        ])

        class Meta:
            model = HelpTextString
            fields = ['model_label']

    class HelpTextSnippetViewSet(SnippetViewSet):
        model = HelpTextString
        menu_label = "Help text"
        icon = "help"
        add_to_settings_menu = True
        list_display = ('identifier', 'model_label', 'text')
        search_fields = ('identifier', 'model_label', 'text')
        filterset_class = HelpTextFilterSet
        url_prefix = 'wagtail_editable_help/helptextstring'

        def get_queryset(self, request):
            # On first call to any ModelAdmin view that retrieves the queryset,
            # ensure that all HelpText definitions in the code have been turned into
            # HelpTextString records in the database
            global _has_populated_records
            if not _has_populated_records:
                populate_help_text_strings()
                _has_populated_records = True

            return super().get_queryset(request)

    register_snippet(HelpTextSnippetViewSet)


@hooks.register("insert_global_admin_css")
def editable_help_css():
    return format_html('<link rel="stylesheet" href="{}">', static('wagtail_editable_help/wagtail_editable_help.css'))
