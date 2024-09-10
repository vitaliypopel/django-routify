from django.urls import path
from django.http import HttpResponse

from abc import ABC, abstractmethod


class RouterAbstraction(ABC):
    '''
        Abstract class for Router.
        Do not use it in your project!

        Attributes:
            app_name: str | None                := Application name same as app_name in urls.py
            urls: list[path]                    := Urls list that can be included in urlpatterns
            auto_naming: bool = True            := Auto naming for every view
            auto_trailing_slash: bool = False   := Auto trailing slash for every view path
    '''

    app_name: str | None
    'Application name same as app_name in urls.py'
    urls: list[path]
    'Urls list that can be included in urlpatterns'

    auto_naming: bool
    'Auto naming for every view | By default equals True'
    auto_trailing_slash: bool
    'Auto trailing slash for every view path | By default equals False'

    @abstractmethod
    def __init__(
            self,
            app_name: str = None,
            auto_naming: bool = True,
            auto_trailing_slash: bool = False,
    ) -> None:
        '''
            Initial method for Router.
            Do not use it in your project!
            This is just abstraction class for Router, without implementation.
            :param app_name: str | None
            :param auto_naming: bool
            :param auto_trailing_slash: bool
        '''
        ...

    @abstractmethod
    def route(self, url_path: str, name: str = None) -> HttpResponse:
        '''
            Router method that register view in urlpatterns with django.urls.path
            :param url_path: str
            :param name: str | None
            :return: HttpResponse
        '''
        ...
