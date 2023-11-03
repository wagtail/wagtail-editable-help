# Wagtail Editable Help

Make help text editable in the Wagtail admin


[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

[![PyPI version](https://badge.fury.io/py/wagtail-editable-help.svg)](https://badge.fury.io/py/wagtail-editable-help)
[![Editable Help CI](https://github.com/wagtail/wagtail-editable-help/actions/workflows/test.yml/badge.svg)](https://github.com/wagtail/wagtail-editable-help/actions/workflows/test.yml)

## Links

- [Documentation](https://github.com/wagtail/wagtail-editable-help/blob/main/README.md)
- [Changelog](https://github.com/wagtail/wagtail-editable-help/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/wagtail/wagtail-editable-help/blob/main/CHANGELOG.md)
- [Discussions](https://github.com/wagtail/wagtail-editable-help/discussions)
- [Security](https://github.com/wagtail/wagtail-editable-help/security)

## Supported versions

- Python 3.8 - 3.12
- Django 3.2 - 4.2
- Wagtail 4.1 - 5.2

## Installation

- Run `pip install wagtail-editable-help`
- Add `"wagtail_editable_help"` to INSTALLED_APPS
- For Wagtail 5.1 and below: add `"wagtail.contrib.modeladmin"` to INSTALLED_APPS if not already present
- Run `./manage.py migrate`
- Optional: add `"wagtail_editable_help.middleware.EditableHelpMiddleware"` to the MIDDLEWARE setting, somewhere below `"django.contrib.auth.middleware.AuthenticationMiddleware"`. Enabling this middleware will add an "Edit" link at the point the help text is shown, to allow superusers and other users with the appropriate permission to edit the help text.

## Usage

For any `help_text` argument that you wish to make editable:

    from wagtail_editable_help.models import HelpText

then replace `help_text="Some help text"` with `help_text=HelpText("model", "identifier", default="Some help text")`. The model and identifier strings serve as a unique identifer for the help text string and to organise the strings in the admin interface - they do not need to exactly match the model or field name. `HelpText` is valid within any definition that supports help text strings, not just model fields - such as form fields and StreamField blocks.

For example:

    class HomePage(Page):
        tagline = models.CharField(max_length=255, help_text="Write something snappy here")

could be rewritten to:

    from wagtail_editable_help.models import HelpText

    class HomePage(Page):
        tagline = models.CharField(max_length=255, help_text=HelpText("Home page", "tagline", default="Write something snappy here"))

The help text string will then be made available for editing within the Wagtail admin under Settings -> Help text, under the heading "Home page tagline".
