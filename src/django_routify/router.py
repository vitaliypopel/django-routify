from typing import Callable

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
        self.__prefix = prefix or ''
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
        def register(view: Callable):
            nonlocal url_path, name
            def inner(*args, **kwargs):
                nonlocal url_path, name, view

                if self.__auto_naming and not name:
                    name = view.__name__.lower().rstrip('View')

                if self.__auto_trailing_slash:
                    url_path = url_path.lstrip('/').rstrip('/') + '/'

                if url_path == '/':
                    url_path = ''

                if isinstance(view, View):
                    view = view.as_view()

                self.__urls.append(
                    path(url_path, view, name=name),
                )

                return view(*args, **kwargs)
            return inner
        return register
