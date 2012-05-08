from django.conf.urls.defaults import *

from .views import page


urlpatterns = patterns("",
    url(
        regex=r"^mount[/]*(?P<file_path>.*)$",
        view=page,
        kwargs=dict(
            directory="filepages",
        ),
    ),
    url(
        regex=r"^(?P<file_path>.*)$",
        view=page,
        kwargs=dict(
            templates_dir=["filepages", "other/filepages"],
        ),
    ),
)
