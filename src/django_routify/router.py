from inspect import isclass
from typing import Callable, Type
import re

from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.views import View

from ._abstraction import RouterAbstraction


class Router(RouterAbstraction):
    '''
        Router class for routing your views.

        Attributes:
            __app_name: str | None              := Application name same as app_name in urls.py
            __prefix: str                       := Prefix for each url paths
            __urls: list[path]                  := Urls list that can be included in urlpatterns
            __auto_naming: bool = True          := Auto naming for every view
            __auto_trailing_slash: bool = False := Auto trailing slash for every view path
    '''

    def __init__(
            self,
            prefix: str = None,
            app_name: str = None,
            auto_naming: bool = True,
            auto_trailing_slash: bool = False,
    ) -> None:
        self.__prefix = prefix.rstrip('/').lstrip('/') or ''
        if self.__prefix != '':
            self.__prefix += '/'
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
    def auto_naming(self) -> bool:
        return self.__auto_naming

    @property
    def auto_trailing_slash(self) -> bool:
        return self.__auto_trailing_slash

    @property
    def urls(self) -> list[path]:
        return self.__urls

    def route(self, url_path: str, name: str = None):
        FUNC_VIEW: Type = Callable[[HttpRequest, ...], HttpResponse]

        def register(view: FUNC_VIEW | View) -> FUNC_VIEW | View:
            nonlocal url_path, name

            if self.__auto_naming and not name:
                name = view.__name__

                if name[-4:].lower() == 'view':
                    name = name[:-4]

                if isclass(view):
                    name = '_'.join(
                        re.findall(
                            pattern='[A-Z][^A-Z]*',
                            string=name,
                        )
                    )

                name = name.lower()

            if self.__auto_trailing_slash:
                url_path = url_path.lstrip('/').rstrip('/') + '/'

            if url_path == '/':
                url_path = ''

            self.__urls.append(
                path(
                    url_path,
                    view.as_view() if isclass(view) else view,
                    name=name,
                )
            )

            return view
        return register
