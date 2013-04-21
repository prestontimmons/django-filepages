from setuptools import setup, find_packages

DESCRIPTION = """
Route urls to file system templates in Django

See:

https://github.com/prestontimmons/django-filepages
"""


setup(
    name="django-filepages",
    version="1.0.0",
    author="Preston Timmons",
    author_email="prestontimmons@gmail.com",
    url="https://github.com/prestontimmons/django-filepages",
    description="Route urls to file system templates in Django.",
    long_description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
