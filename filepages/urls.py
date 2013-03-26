from django.conf.urls import patterns, url

from .views import page


def filepages_urlpatterns(directory, name=None):
    args = dict(
        regex=r"^(?P<file_path>.*)$",
        view=page,
        kwargs=dict(
            directory=directory,
        ),
    )

    if name:
        args["name"] = name

    return patterns("",
        url(**args),
    )
