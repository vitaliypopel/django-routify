from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.urls import URLPattern, path
from django.views import View

from inspect import isclass
from typing import Callable
import re

from ._abstraction import BaseRouter
from .validator import _validate_type

FUNC_BASED_VIEW: type = Callable[[HttpRequest, ...], HttpResponse]
'FUNC_BASED_VIEW is a type of Django function based views'


class Router(BaseRouter):
    '''
    Router class for routing your views.

    Attributes:
        ALLOWED_METHODS: str                := ALLOWED_METHODS is a valid HTTP methods
        __app_name: str | None              := Application name same as app_name in urls.py
        __prefix: str                       := Prefix for each url paths
        __urls: list[URLPattern]            := List of URLPatterns that can be included in urlpatterns
        __auto_naming: bool = True          := Auto naming for every view
        __auto_trailing_slash: bool = False := Auto trailing slash for every view path
    '''

    def __init__(
        self,
        prefix: str = None,
        app_name: str = None,
        **kwargs,
    ) -> None:
        auto_naming = kwargs.get('auto_naming', True)
        auto_trailing_slash = kwargs.get('auto_trailing_slash', False)

        _validate_type('prefix', prefix, (str, type(None)))
        _validate_type('app_name', app_name, (str, type(None)))
        _validate_type('auto_naming', auto_naming, bool)
        _validate_type('auto_trailing_slash', auto_trailing_slash, bool)

        self.__prefix = prefix or ''
        self.__prefix = self.__prefix.lstrip('/')

        if auto_trailing_slash:
            self.__prefix = self.__prefix.rstrip('/') + '/'

        if self.__prefix == '/':
            self.__prefix = ''

        self.__app_name = app_name or ''
        self.__auto_naming = auto_naming
        self.__auto_trailing_slash = auto_trailing_slash

        self.__urls = []

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def app_name(self) -> str:
        return self.__app_name

    @property
    def urls(self) -> list[URLPattern]:
        return self.__urls

    @property
    def auto_naming(self) -> bool:
        return self.__auto_naming

    @property
    def auto_trailing_slash(self) -> bool:
        return self.__auto_trailing_slash

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

            if self.__auto_trailing_slash:
                url_path = url_path.lstrip('/').rstrip('/')
                if url_path != '':
                    url_path += '/'

            if url_path == '/' and self.__prefix[-1:] == '/':
                url_path = ''

            if self.__auto_naming and not name:
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

            self.__urls.append(
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
               f'\tapp_name:\t"{self.__app_name}"\n' \
               f'\turl_prefix:\t"{self.__prefix}"\n' \
               f'\turls:\t\t{self.__urls}\n' \
               f')'

    def __repr__(self) -> str:
        return str(self)
