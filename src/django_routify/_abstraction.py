from abc import ABC, abstractmethod

from django.urls import URLPattern

from .patterns import Pattern


class BasePattern(ABC):
    pass


class BaseRouter(ABC):
    '''
        Abstract class for Router.
        Do not use it in your project!

        Attributes:
            __app_name: str | None              := Application name same as app_name in urls.py
            __prefix: str                       := Prefix for each url paths
            __urls: list[URLPattern]            := List of URLPatterns that can be included in urlpatterns
            __auto_naming: bool = True          := Auto naming for every view
            __auto_trailing_slash: bool = False := Auto trailing slash for every view path
            __dynamic_pattern: Pattern          := ...
    '''

    __app_name: str | None
    'Application name same as app_name in urls.py'
    __prefix: str
    'Prefix for each url paths | By default equals ""'
    __urls: list[URLPattern]
    'List of URLPatterns that can be included in urlpatterns'

    __auto_naming: bool
    'Auto naming for every view | By default equals True'
    __auto_trailing_slash: bool
    'Auto trailing slash for every view path | By default equals False'
    __dynamic_pattern: Pattern
    '''...'''

    @abstractmethod
    def __init__(
        self,
        prefix: str = None,
        app_name: str = None,
        **kwargs,
    ) -> None:
        '''
            Initial method for Router.
            :param prefix: str | None
            :param app_name: str | None
            :param kwargs: Any
        '''
        pass

    @property
    @abstractmethod
    def prefix(self) -> str:
        '''
            prefix getter\n
            Prefix for each url paths
            :return: str
        '''
        pass

    @property
    @abstractmethod
    def app_name(self) -> str:
        '''
            app_name getter\n
            Application name same as app_name in urls.py
            :return: str
        '''
        pass

    @property
    @abstractmethod
    def urls(self) -> list[URLPattern]:
        '''
            urls getter\n
            List of URLPatterns that can be included in urlpatterns
            :return: list[django.urls.URLPattern]
        '''
        pass

    @property
    @abstractmethod
    def auto_naming(self) -> bool:
        '''
            auto_naming getter\n
            Auto naming for every view
            :return: bool
        '''
        pass

    @property
    @abstractmethod
    def auto_trailing_slash(self) -> bool:
        '''
            auto_trailing_slash getter\n
            Auto trailing slash for every view path
            :return: bool
        '''
        pass

    @property
    @abstractmethod
    def dynamic_pattern(self) -> Pattern:
        '''
            ...
            :return: BasePattern
        '''
        pass

    @abstractmethod
    def route(self, url_path: str, **kwargs):
        '''
            Router method that register view in urlpatterns with django.urls.path
            :param url_path: str
            :param kwargs: Any
            :return: Any
        '''
        pass

    @abstractmethod
    def __str__(self) -> str:
        '''
            Router string representation
            :return: str
        '''
        pass

    @abstractmethod
    def __repr__(self) -> str:
        '''
            Router string representation
            :return: str
        '''
        pass
