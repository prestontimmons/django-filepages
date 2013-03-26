from django.conf.urls import patterns, url

from .urls import filepages_urlpatterns
from .views import page


urlpatterns = patterns("",
    url(
        regex=r"^mount[/]*(?P<file_path>.*)$",
        view=page,
        kwargs=dict(
            directory="filepages",
        ),
    ),
)

urlpatterns += filepages_urlpatterns(
    directory=["filepages", "other/filepages"],
)
