# Django-Routify
**Django-Routify** is a lightweight package designed to simplify routing views in the classic Django framework.

With Django-Routify, you no longer need to manually register your views in `urlpatterns` using Django's `path()` function. Instead, the package introduces the `Router` class, allowing you to easily register views using the `@Router.route(url_path=...)` decorator. This approach is similar to what you might already be familiar with from frameworks like Flask, FastAPI, or Django REST Framework (DRF), where views are registered with decorators. This not only makes your code easier to read but also streamlines the process of routing.

Additionally, Django-Routify provides the option to set `auto_trailing_slash=True` when initializing the `Router`. This allows you to write URL paths similar to those in Flask or FastAPI, such as `/hello-world`, which will be automatically translated into the classic Django URL format: `hello-world/`.

Django-Routify supports both `function-based` and `class-based` views, as well as `asynchronous` views, providing flexibility for different project needs. 

## Documentation
Documentation are already available [here](https://vitaliypopel.github.io/django-routify-docs/homepage)!

## Example
For **extended example** with tests visit [examples/example](https://github.com/vitaliypopel/django-routify/tree/main/examples/example).

### Using Django-Routify with Django

~/project/app/views.py:
```python
from django.http import HttpRequest, HttpResponse

from django_routify import Router

router = Router('/app', 'app', auto_trailing_slash=True)


@router.route('/hello-world', methods=['GET']) # or @router.get('/hello-world')
def hello_world(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello World!')
```

~/project/app/urls.py:
```python
from django_routify import include_router

from .views import router

urlpatterns = [
    include_router(router),
]
```

### Using classic Django

~/project/app/views.py:
```python
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def hello_world(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello World!')
```

~/project/app/urls.py:
```python
from django.urls import path, include

from .views import hello_world

app_name = 'app'
urlpatterns = [
    path(
        'app/',
        include(
            [
                path('hello-world/', hello_world, name='hello_world'),
            ]
        ),
    ),
]
```

#### Note:
_The result of these two examples will do the same thing_

## Requirements
- Python 3.8+
- Django 4.0+

## Installation
To install Django-Routify package use the command below in your environment:

- Using `pip`
```shell
pip install django-routify
```

- Using `Poetry`
```shell
poetry add django-routify
```
