from django.conf.urls.defaults import *


urlpatterns = patterns('filepages.views',
    url(r'^(?P<file_path>[^\.]*)/$', 'page',
        dict(base_directory_list=['filepages', 'other/filepages'])),
)
