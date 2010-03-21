# coding=utf-8

import os

from django.conf import settings
from django.test import TestCase

from filepages.sitemap import FilePageSiteMap
from filepages.tests.testcases import BaseViewTestCase


class ViewTestCase(BaseViewTestCase):
    templates = [
        '404.html',
        'filepages/_base.html',
        'filepages/about.html',
        'filepages/base.html',
        'filepages/index.html',
        'filepages/nonhtml.txt',
        'filepages/sub/contact.html',
        'filepages/includes/blurb.html',
        'filepages/get_involved/index.html',
        'other/filepages/other.html',
        'subsite/filepages/about.html',
        'subsite/filepages/index.html',
    ]


class FilePageSiteMapTest(ViewTestCase):

    def test_items(self):
        sitemap = FilePageSiteMap([
            dict(
                base_url="/",
                template_directory="%s/filepages/" % \
                    settings.TEMPLATE_DIRS[0],
            ),
        ])
        self.failUnlessEqual(len(sitemap.items()), 4)

        urls = ['/', '/about/', '/get_involved/', '/sub/contact/']
        for x in sitemap.items():
            self.assert_(x.get_absolute_url() in urls)


class PageTest(ViewTestCase):

    urls = 'filepages.tests.urls'

    def test_flat_page_from_file(self):
        response = self.client.get("/about/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/about.html")

        response = self.client.get("/sub/contact/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/sub/contact.html")

        response = self.client.get("/get_involved/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "filepages/get_involved/index.html")

        response = self.client.get("/other/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "other/filepages/other.html")

    def test_dots_not_allowed(self):
        response = self.client.get("/sub/../about/")
        self.failUnlessEqual(response.status_code, 404)

    def test_ignore_files_starting_with_base_(self):
        response = self.client.get("/base/")
        self.failUnlessEqual(response.status_code, 404)

    def test_ignore_includes_directory(self):
        response = self.client.get("/includes/blurb/")
        self.failUnlessEqual(response.status_code, 404)

    def test_ignore_files_starting_with_underscores(self):
        response = self.client.get("/_base/")
        self.failUnlessEqual(response.status_code, 404)

    def test_404_raised_if_no_file_exists(self):
        response = self.client.get("/does_not_exist/")
        self.failUnlessEqual(response.status_code, 404)

    def test_404_for_non_ascii_url(self):
        response = self.client.get("/¤/")
        self.failUnlessEqual(response.status_code, 404)
