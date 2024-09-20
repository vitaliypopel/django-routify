from django.http import HttpRequest, HttpResponse
from django.urls import path

from abc import ABC, abstractmethod
from typing import Callable, Type

FUNC_VIEW: Type = Callable[[HttpRequest, ...], HttpResponse]


class RouterAbstraction(ABC):
    '''
        Abstract class for Router.
        Do not use it in your project!

        Attributes:
            __app_name: str | None              := Application name same as app_name in urls.py
            __prefix: str                       := Prefix for each url paths
            __urls: list[path]                  := Urls list that can be included in urlpatterns
            __auto_naming: bool = True          := Auto naming for every view
            __auto_trailing_slash: bool = False := Auto trailing slash for every view path
    '''

    __app_name: str | None
    'Application name same as app_name in urls.py'
    __prefix: str
    'Prefix for each url paths | By default equals ""'
    __urls: list[path]
    'Urls list that can be included in urlpatterns'

    __auto_naming: bool
    'Auto naming for every view | By default equals True'
    __auto_trailing_slash: bool
    'Auto trailing slash for every view path | By default equals False'

    @abstractmethod
    def __init__(
            self,
            prefix: str = None,
            app_name: str = None,
            auto_naming: bool = True,
            auto_trailing_slash: bool = False,
    ) -> None:
        '''
            Initial method for Router.
            :param: prefix: str
            :param app_name: str | None
            :param auto_naming: bool
            :param auto_trailing_slash: bool
        '''
        raise NotImplementedError(
            'Use Router from django_routify, '
            'but not RouterAbstraction'
        )

    @property
    @abstractmethod
    def prefix(self) -> str:
        '''
            prefix getter\n
            Prefix for each url paths
            :return: str
        '''
        ...

    @property
    @abstractmethod
    def app_name(self) -> str:
        '''
            app_name getter\n
            Application name same as app_name in urls.py
            :return: str
        '''
        ...

    @property
    @abstractmethod
    def auto_naming(self) -> bool:
        '''
            auto_naming getter\n
            Auto naming for every view
            :return: bool
        '''
        ...

    @property
    @abstractmethod
    def auto_trailing_slash(self) -> bool:
        '''
            auto_trailing_slash getter\n
            Auto trailing slash for every view path
            :return: bool
        '''
        ...

    @property
    @abstractmethod
    def urls(self) -> list[path]:
        '''
            urls getter\n
            Urls list that can be included in urlpatterns
            :return: list[path]
        '''
        ...

    @abstractmethod
    def route(self, url_path: str, name: str = None):
        '''
            Router method that register view in urlpatterns with django.urls.path
            :param url_path: str
            :param name: str | None
            :return: Any
        '''
        ...

    @abstractmethod
    def __str__(self) -> str:
        '''
            Router string representation
            :return: str
        '''
        ...

    @abstractmethod
    def __repr__(self) -> str:
        '''
            Router string representation
            :return: str
        '''
        ...
