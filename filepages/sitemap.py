import datetime
import os

from django.contrib.sitemaps import Sitemap

from filepages.views import is_safe


def templates_in_directory(directory):
    templates = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            f = os.path.join(root, f)
            if is_safe(f) and f.endswith(".html"):
                templates.append(f.replace(directory, ""))
    return templates


class FilePageObject(object):

    def __init__(self, base_url, template_directory, template):
        self.base_url = base_url
        self.template_directory = template_directory
        self.template = template
        self.url = self.resolve_url()

    def resolve_url(self):
        url = "%s/%s/" % (self.base_url, self.template[:-5])
        url = url.replace("//", "/")
        return url.replace("/index/", "/")

    def get_absolute_url(self):
        return self.url


class FilePageSiteMap(Sitemap):

    def __init__(self, url_to_directory_map):
        self.url_map = url_to_directory_map

    def items(self):
        page_objects = []
        for entry in self.url_map:
            templates = templates_in_directory(entry["template_directory"])
            for template in templates:
                page_objects.append(FilePageObject(entry["base_url"],
                    entry["template_directory"], template))
        return page_objects

    def lastmod(self, obj):
        return datetime.datetime.fromtimestamp(
            os.path.getmtime(os.path.join(obj.template_directory,
                obj.template)))
