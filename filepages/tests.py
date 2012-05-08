# coding=utf-8

from django.test import TestCase
from django.test.utils import (
    restore_template_loaders,
    setup_test_template_loader,
)


class PageViewTest(TestCase):
    urls = "filepages.test_urls"

    def setUp(self):
        setup_test_template_loader({
            "404.html": "",
            "filepages/about.html": "",
            "filepages/sub/contact.html": "",
            "filepages/get_involved/index.html": "",
            "other/filepages/other.html": "",
        })

    def tearDown(self):
        restore_template_loaders()

    def test_page(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/about.html")

        response = self.client.get("/sub/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/sub/contact.html")

        response = self.client.get("/get_involved/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/get_involved/index.html")

        response = self.client.get("/other/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "other/filepages/other.html")

        response = self.client.get("/mount/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/about.html")

    def test_dots_not_allowed(self):
        response = self.client.get("/sub/../about/")
        self.assertEqual(response.status_code, 404)

    def test_ignore_files_starting_with_base_(self):
        response = self.client.get("/base/")
        self.assertEqual(response.status_code, 404)

    def test_ignore_includes_directory(self):
        response = self.client.get("/includes/blurb/")
        self.assertEqual(response.status_code, 404)

    def test_ignore_files_starting_with_underscores(self):
        response = self.client.get("/_base/")
        self.assertEqual(response.status_code, 404)

    def test_404_raised_if_no_file_exists(self):
        response = self.client.get("/does_not_exist/")
        self.assertEqual(response.status_code, 404)

    def test_404_for_non_ascii_url(self):
        response = self.client.get("/¤/")
        self.assertEqual(response.status_code, 404)
