from os.path import basename, join

from django.http import Http404

from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.template.response import TemplateResponse


try:
    str_type = base_string  # PY2
except NameError:
    str_type = str


def is_safe(file_path):
    try:
        file_path.encode("ascii")
    except UnicodeEncodeError:
        return False

    base_name = basename(file_path)
    return not any((
        base_name.startswith("_"),
        base_name.startswith("base"),
        ".." in file_path,
        "includes" in file_path,
    ))


def page(request, file_path, directory=None, templates_dir=None):
    file_path = file_path or "index"
    file_path = file_path.strip("/")

    if not is_safe(file_path):
        raise Http404

    directory = directory or templates_dir
    if isinstance(directory, str_type):
        directory = [directory]

    directories = []
    for directory in directory:
        directories.extend([
            "%s/index.html" % join(directory, file_path),
            "%s.html" % join(directory, file_path),
        ])

    try:
        template = select_template(directories)
    except TemplateDoesNotExist:
        message = (
            "File page not found or bad include line in template."
            "Looked in: %s" % directories
        )
        raise Http404(message)

    return TemplateResponse(request, template)
