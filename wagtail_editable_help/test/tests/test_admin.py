from django.contrib.auth.models import Group, User
from django.test import TestCase

try:
    from wagtail.models import Page
except ImportError:
    from wagtail.core.models import Page

from wagtail_editable_help.models import HelpTextString


class TestAdmin(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser("admin", "admin@example.com", "password")
        self.normal_user = User.objects.create_user("ed", "ed@example.com", "password")
        self.normal_user.groups.add(Group.objects.get(name="Editors"))
        self.root_page = Page.objects.get(depth=2)

    def test_get_default_text(self):
        self.assertEqual(HelpTextString.objects.count(), 0)

        self.client.login(username="admin", password="password")
        response = self.client.get(
            "/admin/pages/add/wagtail_editable_help_test/homepage/%d/" % self.root_page.id
        )
        self.assertEqual(response.status_code, 200)

        # with no pre-existing HelpTextString record, the default text should be shown
        self.assertContains(response, "Write something snappy here")

        # a new HelpTextString record now exists
        self.assertEqual(HelpTextString.objects.count(), 1)

    def test_get_alternative_text(self):
        help_text = HelpTextString.objects.create(
            model_label="Home page", identifier="tagline", text="Write something clickbaity here"
        )
        self.client.login(username="admin", password="password")
        response = self.client.get(
            "/admin/pages/add/wagtail_editable_help_test/homepage/%d/" % self.root_page.id
        )
        self.assertEqual(response.status_code, 200)

        # Help text should pick up the custom HelpTextString record
        self.assertNotContains(response, "Write something snappy here")
        self.assertContains(response, "Write something clickbaity here")

        # superuser should get the Edit link
        self.assertContains(response, '(<a href="/admin/wagtail_editable_help/helptextstring/edit/%d/">Edit</a>)' % help_text.id)

        self.assertEqual(HelpTextString.objects.count(), 1)

    def test_get_alternative_text_as_normal_user(self):
        help_text = HelpTextString.objects.create(
            model_label="Home page", identifier="tagline", text="Write something clickbaity here"
        )
        self.client.login(username="ed", password="password")
        response = self.client.get(
            "/admin/pages/add/wagtail_editable_help_test/homepage/%d/" % self.root_page.id
        )
        self.assertEqual(response.status_code, 200)

        # Help text should pick up the custom HelpTextString record
        self.assertNotContains(response, "Write something snappy here")
        self.assertContains(response, "Write something clickbaity here")

        # normal user without edit permission on HelpTextString should not get the Edit link
        self.assertNotContains(response, '(<a href="/admin/wagtail_editable_help/helptextstring/edit/%d/">Edit</a>)' % help_text.id)

        self.assertEqual(HelpTextString.objects.count(), 1)

    def test_help_text_strings_index(self):
        self.client.login(username="admin", password="password")
        response = self.client.get("/admin/wagtail_editable_help/helptextstring/")
        self.assertEqual(response.status_code, 200)

        # The listing should contain all defined HelpTextString records,
        # even if we never triggered their creation by visiting a view that rendered them
        self.assertContains(response, "Home page")
        self.assertContains(response, "tagline")
        self.assertContains(response, "Write something snappy here")
