import os
import shutil
import tempfile

from django.conf import settings
from django.test import TestCase
from django.test.client import Client


class BaseViewTestCase(TestCase):

    templates =  []
    REMOTE_ADDR = "127.0.0.1"
    HTTP_HOST = "localhost"
    HTTP_USER_AGENT = "Django Test Client"
    HTTP_REFERER = "None"
    SERVER_NAME = "localhost"

    def setUp(self):
        self.client = Client(
            REMOTE_ADDR=self.REMOTE_ADDR,
            HTTP_HOST=self.HTTP_HOST,
            HTTP_USER_AGENT=self.HTTP_USER_AGENT,
            HTTP_REFERER=self.HTTP_REFERER,
            SERVER_NAME=self.SERVER_NAME,
        )

        directory_name = tempfile.mkdtemp()
        for path in self.templates:
            if os.path.dirname(path):
                newdir = os.path.join(directory_name,
                    os.path.dirname(path))
                if not os.path.isdir(newdir):
                    os.makedirs(newdir)
            handle = open(os.path.join(directory_name, path), 'w')
            handle.close()

        self.TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (directory_name, )

    def tearDown(self):
        shutil.rmtree(settings.TEMPLATE_DIRS[0])
        settings.TEMPLATE_DIRS = self.TEMPLATE_DIRS
