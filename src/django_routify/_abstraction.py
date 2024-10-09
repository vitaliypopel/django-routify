from abc import ABC, abstractmethod
from typing import Any

from django.urls import URLPattern


class BasePattern(ABC):
    """
    Abstract class for Pattern.
    Do not use it in your project!

    Attributes:
        REGEX: str      := Regular expression for parsing url
    """

    REGEX: str
    'Regular expression for parsing url | By default REGEX equals ""'

    @abstractmethod
    def normalize(
        self,
        custom_url: str,
        view: Any,
        class_based: bool,
    ) -> str:
        """
        Method for normalizing url using REGEX.
        Returns url with Django format style.
        :param custom_url: str
        :param view: FUNC_BASED_VIEW | View
        :param class_based: bool
        :return: str
        """
        pass

    @abstractmethod
    def _get_url_params(self, custom_url: str) -> list[str]:
        """
        Method for getting url params from custom url
        :param custom_url: str
        :return: list[str]
        """
        pass

    @abstractmethod
    def _get_dynamic_params(self, custom_url: str) -> list[str]:
        """
        Method for getting full dynamic params from custom url
        :param custom_url: str
        :return: list[str]
        """
        pass

    @abstractmethod
    def is_custom(self, url_: str) -> bool:
        """
        Is url has params from current pattern
        :param url_: str
        :return: bool
        """

    @staticmethod
    @abstractmethod
    def _get_annotations(
        view: Any,
        class_based: bool,
    ) -> dict[str, type]:
        """
        Method for getting annotations from difference types of views
        :param view: Any
        :param class_based: bool
        :return: dict[str, str]
        """
        pass

    @staticmethod
    @abstractmethod
    def _get_django_type(python_type: type) -> str:
        """
        Method for getting Django type for dynamic URL from Python type
        :param python_type: type
        :return: str
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Pattern string representation
        :return: str
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Pattern string representation
        :return: str
        """
        pass


from .patterns import Pattern


class BaseRouter(ABC):
    """
    Abstract class for Router.
    Do not use it in your project!

    Attributes:
        ALLOWED_METHODS: str                := ALLOWED_METHODS is a valid HTTP methods
        __app_name: str | None              := Application name same as app_name in urls.py
        __prefix: str                       := Prefix for each url paths
        __urls: list[URLPattern]            := List of URLPatterns that can be included in urlpatterns
        __auto_naming: bool = True          := Auto naming for every view
        __auto_trailing_slash: bool = False := Auto trailing slash for every view path
        __dynamic_pattern: Pattern          := Dynamic pattern for parsing and normalizing custom urls
    """

    ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    'ALLOWED_METHODS is a valid HTTP methods'

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
    'Dynamic pattern for parsing and normalizing custom urls | By default equals None'

    @abstractmethod
    def __init__(
        self,
        prefix: str = None,
        app_name: str = None,
        **kwargs,
    ) -> None:
        """
        Initial method for Router.
        :param prefix: str | None
        :param app_name: str | None
        :param kwargs: Any
        """
        pass

    @property
    @abstractmethod
    def prefix(self) -> str:
        """
        prefix getter\n
        Prefix for each url paths
        :return: str
        """
        pass

    @property
    @abstractmethod
    def app_name(self) -> str:
        """
        app_name getter\n
        Application name same as app_name in urls.py
        :return: str
        """
        pass

    @property
    @abstractmethod
    def urls(self) -> list[URLPattern]:
        """
        urls getter\n
        List of URLPatterns that can be included in urlpatterns
        :return: list[django.urls.URLPattern]
        """
        pass

    @property
    @abstractmethod
    def auto_naming(self) -> bool:
        """
        auto_naming getter\n
        Auto naming for every view
        :return: bool
        """
        pass

    @property
    @abstractmethod
    def auto_trailing_slash(self) -> bool:
        """
        auto_trailing_slash getter\n
        Auto trailing slash for every view path
        :return: bool
        """
        pass

    @property
    @abstractmethod
    def dynamic_pattern(self) -> Pattern:
        """
        dynamic_pattern getter\n
        Dynamic pattern for parsing and normalizing custom urls
        :return: django_routify.patterns.Pattern
        """
        pass

    @abstractmethod
    def route(self, url_path: str, **kwargs):
        """
        Router method that register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Any
        :return: Any
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Router string representation
        :return: str
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Router string representation
        :return: str
        """
        pass
