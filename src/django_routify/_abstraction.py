from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    Union,
)

from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern
from django.views import View


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
        :param view: Union[FUNC_BASED_VIEW, View]
        :param class_based: bool
        :return: str
        """
        pass

    @abstractmethod
    def _get_url_params(self, custom_url: str) -> List[str]:
        """
        Method for getting url params from custom url
        :param custom_url: str
        :return: List[str]
        """
        pass

    @abstractmethod
    def _get_dynamic_params(self, custom_url: str) -> List[str]:
        """
        Method for getting full dynamic params from custom url
        :param custom_url: str
        :return: List[str]
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
    ) -> Dict[str, Type]:
        """
        Method for getting annotations from difference types of views
        :param view: Any
        :param class_based: bool
        :return: Dict[str, Type]
        """
        pass

    @staticmethod
    @abstractmethod
    def _get_django_type(python_type: Type) -> str:
        """
        Method for getting Django type for dynamic URL from Python type
        :param python_type: Type
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


from .validator import _validate_type
from .patterns import (
    Pattern,
    ColonPattern,
    CurlyPattern,
    AnglePattern,
)

FUNC_BASED_VIEW: Type = Callable[[HttpRequest], HttpResponse]
'FUNC_BASED_VIEW is a type of Django function based views'


class BaseRouter(ABC):
    """
    Abstract class for Router.
    Do not use it in your project!

    Attributes:
        ALLOWED_METHODS: str                := ALLOWED_METHODS is a valid HTTP methods
        __app_name: Optional[str]           := Application name same as app_name in urls.py
        __prefix: str                       := Prefix for each url paths
        __urls: List[URLPattern]            := List of URLPatterns that can be included in urlpatterns
        __auto_naming: bool = True          := Auto naming for every view
        __auto_trailing_slash: bool = False := Auto trailing slash for every view path
        __dynamic_pattern: Pattern          := Dynamic pattern for parsing and normalizing custom urls
    """

    ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    'ALLOWED_METHODS is a valid HTTP methods'

    __app_name: Optional[str]
    'Application name same as app_name in urls.py'
    __prefix: str
    'Prefix for each url paths | By default equals ""'
    __urls: List[URLPattern]
    'List of URLPatterns that can be included in urlpatterns'

    __auto_naming: bool
    'Auto naming for every view | By default equals True'
    __auto_trailing_slash: bool
    'Auto trailing slash for every view path | By default equals False'
    __dynamic_pattern: Pattern
    'Dynamic pattern for parsing and normalizing custom urls | By default equals None'

    def __init__(
        self,
        prefix: str = None,
        app_name: str = None,
        **kwargs,
    ) -> None:
        """
        Initial method for Router.
        :param prefix: Optional[str]
        :param app_name: Optional[str]
        :param kwargs: Any
        """

        auto_naming = kwargs.get('auto_naming', True)
        auto_trailing_slash = kwargs.get('auto_trailing_slash', False)
        dynamic_pattern = kwargs.get('dynamic_pattern', Pattern)()

        _validate_type('prefix', prefix, (str, type(None)))
        _validate_type('app_name', app_name, (str, type(None)))
        _validate_type('auto_naming', auto_naming, bool)
        _validate_type('auto_trailing_slash', auto_trailing_slash, bool)
        _validate_type(
            'dynamic_pattern',
            dynamic_pattern,
            (Pattern, ColonPattern, CurlyPattern, AnglePattern),
        )

        self.__prefix = prefix or ''
        self.__prefix = self.__prefix.lstrip('/')

        if auto_trailing_slash:
            self.__prefix = self.__prefix.rstrip('/') + '/'

        if self.__prefix == '/':
            self.__prefix = ''

        self.__app_name = app_name or ''
        self.__auto_naming = auto_naming
        self.__auto_trailing_slash = auto_trailing_slash
        self.__dynamic_pattern = dynamic_pattern

        self.__urls = []

    @property
    def prefix(self) -> str:
        """
        prefix getter\n
        Prefix for each url paths
        :return: str
        """
        return self.__prefix

    @property
    def app_name(self) -> str:
        """
        app_name getter\n
        Application name same as app_name in urls.py
        :return: str
        """
        return self.__app_name

    @property
    def urls(self) -> List[URLPattern]:
        """
        urls getter\n
        List of URLPatterns that can be included in urlpatterns
        :return: List[django.urls.URLPattern]
        """
        return self.__urls

    @property
    def auto_naming(self) -> bool:
        """
        auto_naming getter\n
        Auto naming for every view
        :return: bool
        """
        return self.__auto_naming

    @property
    def auto_trailing_slash(self) -> bool:
        """
        auto_trailing_slash getter\n
        Auto trailing slash for every view path
        :return: bool
        """
        return self.__auto_trailing_slash

    @property
    def dynamic_pattern(self) -> Pattern:
        """
        dynamic_pattern getter\n
        Dynamic pattern for parsing and normalizing custom urls
        :return: django_routify.patterns.Pattern
        """
        return self.__dynamic_pattern

    @abstractmethod
    def route(self, url_path: str, **kwargs):
        """
        Router decorator that register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Any
        """
        pass

    @abstractmethod
    def get(self, url_path: str, **kwargs):
        """
        Router decorator that wrap view into require GET decorator and
        register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Any
        """
        pass

    @abstractmethod
    def post(self, url_path: str, **kwargs):
        """
        Router decorator that wrap view into require POST decorator and
        register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Any
        """
        pass

    @abstractmethod
    def put(self, url_path: str, **kwargs):
        """
        Router decorator that wrap view into require PUT decorator and
        register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Any
        """
        pass

    @abstractmethod
    def patch(self, url_path: str, **kwargs):
        """
        Router decorator that wrap view into require PATCH decorator and
        register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Any
        """
        pass

    @abstractmethod
    def delete(self, url_path: str, **kwargs):
        """
        Router decorator that wrap view into require DELETE decorator and
        register view in urlpatterns with django.urls.path
        :param url_path: str
        :param kwargs: Dict[str, Any]
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
