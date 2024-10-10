from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.urls import path
from django.views import View

from inspect import isclass
from typing import Callable
import re

from ._abstraction import BaseRouter
from .validator import _validate_type

FUNC_BASED_VIEW: type = Callable[[HttpRequest, ...], HttpResponse]
'FUNC_BASED_VIEW is a type of Django function based views'


class Router(BaseRouter):
    """
    Router class for routing your views.

    Attributes:
        ALLOWED_METHODS: str                := ALLOWED_METHODS is a valid HTTP methods
        __app_name: str | None              := Application name same as app_name in urls.py
        __prefix: str                       := Prefix for each url paths
        __urls: list[URLPattern]            := List of URLPatterns that can be included in urlpatterns
        __auto_naming: bool = True          := Auto naming for every view
        __auto_trailing_slash: bool = False := Auto trailing slash for every view path
        __dynamic_pattern: Pattern          := Dynamic pattern for parsing and normalizing custom urls
    """

    def route(self, url_path: str, **kwargs):
        def register(view: FUNC_BASED_VIEW | View) -> FUNC_BASED_VIEW | View:
            nonlocal url_path, kwargs

            class_based = False
            if isclass(view) and issubclass(view, View):
                class_based = True

            name: str | None = kwargs.get('name', None)
            methods: list[str] | None = kwargs.get('methods', None)

            _validate_type('url_path', url_path, str)
            _validate_type('name', name, (str, type(None)))
            _validate_type('methods', methods, (list, type(None)))

            if self.dynamic_pattern.is_custom(self.prefix):
                self._BaseRouter__prefix = self.dynamic_pattern.normalize(
                    custom_url=self.prefix,
                    view=view,
                    class_based=class_based,
                )

            if self.auto_trailing_slash:
                url_path = url_path.lstrip('/').rstrip('/')
                if url_path != '':
                    url_path += '/'

            if url_path == '/' and self.prefix[-1:] == '/':
                url_path = ''

            if self.dynamic_pattern.is_custom(url_path):
                url_path = self.dynamic_pattern.normalize(
                    custom_url=url_path,
                    view=view,
                    class_based=class_based,
                )

            if self.auto_naming and not name:
                name = view.__name__

                if class_based:
                    if name[-4:].lower() == 'view':
                        name = name[:-4]

                    name = '_'.join(
                        re.findall(
                            pattern='[A-Z][^A-Z]*',
                            string=name,
                        )
                    )

                name = name.lower()

            if methods:
                for i in range(len(methods)):
                    methods[i] = methods[i].upper()
                    if methods[i] not in self.ALLOWED_METHODS:
                        raise ValueError(
                            f'Method "{methods[i]}" is not in '
                            f'allowed methods {self.ALLOWED_METHODS}'
                        )

                require_http_methods_decorator = require_http_methods(methods)

                if class_based:
                    # wrap Class-Based-View into decorator with require methods
                    # using method_decorator
                    view = method_decorator(
                        decorator=require_http_methods_decorator,
                        name='dispatch',
                    )(view)
                else:
                    # wrap Function-Based-View into decorator with require methods
                    view = require_http_methods_decorator(view)

            as_view = view
            if class_based:
                view: View
                as_view = view.as_view()

            self._BaseRouter__urls.append(
                path(
                    url_path,
                    as_view,
                    name=name,
                )
            )

            return view
        return register

    def __str__(self) -> str:
        return f'Router(\n' \
               f'\tapp_name:\t"{self.app_name}"\n' \
               f'\turl_prefix:\t"{self.prefix}"\n' \
               f'\turls:\t\t{self.urls}\n' \
               f')'

    def __repr__(self) -> str:
        return str(self)
