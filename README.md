# django-rest-extensions
A project that can provide api super super super fast.

# WARNING
**This app will expose all api to the public make sure you have added the correct permission rules**

# TODO
add configurations parameters that allow user to limit which apps or models should generate api

# Install
```
pip install django-rest-extensions
```

# Usage
```
1. add rest_extensions to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    "rest_extensions",
]
2. add url to project.urls
urlpatterns = [
    path('rest_extensions/', include("rest_extensions.urls")),
]
```


# Example
```
cd example
python manage.py runserver
```
