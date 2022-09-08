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

- Python 3.7 - 3.10
- Django 3.2 - 4.1
- Wagtail 2.15 - 4.0

## Installation

- Run `pip install wagtail-editable-help`
- Add `"wagtail_editable_help"` and `"wagtail.contrib.modeladmin"` to INSTALLED_APPS
- Run `./manage.py migrate`
- Optional: add `"wagtail_editable_help.middleware.EditableHelpMiddleware"` to the MIDDLEWARE setting, somewhere below `"django.contrib.auth.middleware.AuthenticationMiddleware"`. Enabling this middleware will add an "Edit" link at the point the help text is shown, to allow superusers and other users with the appropriate permission to edit the help text.

## Usage

For any `help_text` argument that you wish to make editable:

    from wagtail_editable_help import HelpText

then replace `help_text="Some help text"` with `help_text=HelpText("model", "identifier", default="Some help text")`. For example:

    class HomePage(Page):
        tagline = models.CharField(max_length=255, help_text="Write something snappy here")

could be rewritten to:

    from wagtail_editable_help.models import HelpText

    class HomePage(Page):
        tagline = models.CharField(max_length=255, help_text=HelpText("Home page", "tagline", default="Write something snappy here"))

The help text string will then be made available for editing within the Wagtail admin under Settings -> Help text, under the heading "Home page tagline".
