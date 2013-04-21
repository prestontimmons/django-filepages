# Route urls to file system templates in Django.

Set up a url:

```python
from filepages.urls import filepages_urlpatterns

urlpatterns += filepages_urlpatterns(
    directory="filepages/",
    name="filepages",
)
```

Add a template: `filepages/mytemplate.html`.

Load the page at `/mytemplate/`.
