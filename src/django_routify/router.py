from django.urls import URLPattern, path
from django.views import View

from inspect import isclass
import re

from ._abstraction import RouterAbstraction
from ._utils import FUNC_VIEW, validate_type


class Router(RouterAbstraction):
    '''
        Router class for routing your views.

        Attributes:
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
            auto_naming: bool = True,
            auto_trailing_slash: bool = False,
    ) -> None:
        validate_type('prefix', prefix, (str, type(None)))
        validate_type('app_name', app_name, (str, type(None)))
        validate_type('auto_naming', auto_naming, bool)
        validate_type(
            'auto_trailing_slash',
            auto_trailing_slash,
            bool,
        )

        self.__prefix = prefix or ''

        if auto_trailing_slash:
            self.__prefix = self.__prefix.lstrip('/').rstrip('/') + '/'
        else:
            self.__prefix = self.__prefix.lstrip('/')

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
    def auto_naming(self) -> bool:
        return self.__auto_naming

    @property
    def auto_trailing_slash(self) -> bool:
        return self.__auto_trailing_slash

    @property
    def urls(self) -> list[URLPattern]:
        return self.__urls

    def route(self, url_path: str, name: str = None):
        def register(view: FUNC_VIEW | View) -> FUNC_VIEW | View:
            nonlocal url_path, name

            validate_type('url_path', url_path, str)
            validate_type('name', name, (str, type(None)))

            if self.__auto_trailing_slash:
                url_path = url_path.lstrip('/').rstrip('/')
                if url_path != '':
                    url_path += '/'

            if url_path == '/' and self.__prefix[-1:] == '/':
                url_path = ''

            if self.__auto_naming and not name:
                name = view.__name__

                if isclass(view):
                    if name[-4:].lower() == 'view':
                        name = name[:-4]

                    name = '_'.join(
                        re.findall(
                            pattern='[A-Z][^A-Z]*',
                            string=name,
                        )
                    )

                name = name.lower()

            self.__urls.append(
                path(
                    url_path,
                    view.as_view() if isclass(view) else view,
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
