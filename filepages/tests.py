# coding=utf-8

from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings

from filepages.views import is_safe, page


@override_settings(
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                ("django.template.loaders.locmem.Loader", {
                    "404.html": "",
                    "filepages/about.html": "about",
                    "filepages/base.html": "base",
                    "filepages/sub/contact.html": "contact",
                    "filepages/get-involved/index.html": "index",
                    "other/filepages/other.html": "other",
                }),
            ],
        },
    }],
)
class PageViewTest(TestCase):

    def test_path(self):
        request = RequestFactory().get("/about/")
        response = page(request, "/about/", directory="filepages/")
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(response.content.decode("utf-8"), "about")

    def test_directory_path(self):
        request = RequestFactory().get("/sub/contact/")
        response = page(request, "/sub/contact/", directory="filepages/")
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(response.content.decode("utf-8"), "contact")

    def test_index(self):
        request = RequestFactory().get("/get-involved/")
        response = page(request, "/get-involved/", directory="filepages/")
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(response.content.decode("utf-8"), "index")

    def test_multiple_directories(self):
        request = RequestFactory().get("/other/")
        response = page(request, "/other/", directory=[
            "filepages/",
            "other/filepages/",
        ])
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(response.content.decode("utf-8"), "other")

    def test_404(self):
        request = RequestFactory().get("/does-not-exist/")

        with self.assertRaises(Http404):
            page(request, "/does-not-exist/", directory="filepages/")

    def test_404_for_non_ascii_url(self):
        request = RequestFactory().get(u"/¤/")

        with self.assertRaises(Http404):
            page(request, u"/¤/", directory="filepages/")


class IsSafeTest(TestCase):

    def test_valid(self):
        url = "page"
        self.assertTrue(is_safe(url))

    def test_dots_not_allowed(self):
        url = "sub/../about"
        self.assertFalse(is_safe(url))

    def test_ignore_files_starting_with_base(self):
        url = "base"
        self.assertFalse(is_safe(url))

    def test_ignore_includes_directory(self):
        url = "includes/blurb"
        self.assertFalse(is_safe(url))

    def test_ignore_files_starting_with_underscores(self):
        url = "_page"
        self.assertFalse(is_safe(url))
