# Django-Routify
**Django-Routify** is a package for simple routing Views in the classic Django framework.

With Django-Routify package you no longer have to manually register your views in `urlpatterns` using django.urls.path function.

Django-Routify can help you to easily register your views using Router class and his @Router.route(...) decorator.
If you are familiar with Flask, FastAPI or even Django REST Framework, you know that every single view should be registered using decorators.
It is <ins>easy to read</ins> first of all, and <ins>simplified work</ins>.

Also you can set auto_trailing_slash to True value when you're initializing your Router and can write your url_path similar to Flask, FastAPI etc.
If auto_trailing_slash is True then url_path which will be equal to '/hello-world' will be translated to classic Django url rule - 'hello-world/'.

## Example
### Using Django-Routify with Django

~/project/app/views.py:
```python
from django.http import HttpRequest, HttpResponse

from django_routify import Router

router = Router('/app', 'app', auto_trailing_slash=True)
# or   = Router(prefix='/app', app_name='app', auto_trailing_slash=True)


@router.route('/hello-world')
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
        include([
                path('hello-world/', hello_world, name='hello_world'),
        ])
    ),
]
```

#### Note:
_The result of these two examples will do the same thing_

## Installation
To install Django-Routify package use the command below in your environment:

- For Linux/Mac:
```shell
python3 -m pip install django-routify
```
- For Windows:
```shell
python -m pip install django-routify
```
