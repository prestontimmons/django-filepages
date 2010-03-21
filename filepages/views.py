import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext, TemplateDoesNotExist


def file_should_be_ignored(file_path):

    try:
        file_path.encode("ascii")
    except UnicodeEncodeError:
        return True

    return os.path.basename(file_path).startswith("_") or \
        os.path.basename(file_path).startswith("base") or \
        'includes' in file_path


def page(request, base_directory_list, file_path):

    if file_should_be_ignored(file_path):
        raise Http404

    if file_path == "":
        file_path = "index"

    directories = []
    for directory in base_directory_list:
        directories.extend([
            "%s/index.html" % os.path.join(directory, file_path),
            "%s.html" % os.path.join(directory, file_path),
        ])

    try:
        t = loader.select_template(directories)
    except TemplateDoesNotExist:
        message = ''
        if settings.DEBUG:
            message = "Could not find templates %s" % directories
        raise Http404(message)

    return HttpResponse(t.render(RequestContext(request)))
