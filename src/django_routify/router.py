from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.urls import path
from django.views import View

from inspect import isclass
from typing import List, Optional, Union, Literal
import re

from ._abstraction import BaseRouter, FUNC_BASED_VIEW
from .validator import _validate_type


class Router(BaseRouter):
    """
    Router class for routing your views.

    Attributes:
        ALLOWED_METHODS: str                := ALLOWED_METHODS is a valid HTTP methods
        __app_name: Optional[str]           := Application name same as app_name in urls.py
        __prefix: str                       := Prefix for each url paths
        __urls: List[URLPattern]            := List of URLPatterns that can be included in urlpatterns
        __auto_naming: bool = True          := Auto naming for every view
        __auto_trailing_slash: bool = False := Auto trailing slash for every view path
        __dynamic_pattern: Pattern          := Dynamic pattern for parsing and normalizing custom urls
    """

    def __register(
        self,
        view: Union[FUNC_BASED_VIEW, View],
        url_path: str,
        **kwargs,
    ) -> Union[FUNC_BASED_VIEW, View]:
        """
        Private method which register view in Router and returns view
        :param view: Union[FUNC_BASED_VIEW, View]
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Union[FUNC_BASED_VIEW, View]
        """

        class_based = False
        if isclass(view) and issubclass(view, View):
            class_based = True

        name: Optional[str] = kwargs.get('name', None)
        methods: Optional[List[str]] = kwargs.get('methods', None)

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
            as_view = view.as_view()

        self._BaseRouter__urls.append(
            path(
                url_path,
                as_view,
                name=name,
            )
        )

        return view

    def __register_with_single_method(
        self,
        view: Union[FUNC_BASED_VIEW, View],
        url_path: str,
        **kwargs,
    ) -> Union[FUNC_BASED_VIEW, View]:
        """
        Private method which register view in Router,
        wrap it in require HTTP methods with one method
        and returns view
        :param view: Union[FUNC_BASED_VIEW, View]
        :param url_path: str
        :param kwargs: Dict[str, Any]
        :return: Union[FUNC_BASED_VIEW, View]
        """

        method = kwargs.get('method')
        name = kwargs.get('name')

        return self.__register(
            view,
            url_path,
            methods=[method],
            name=name,
        )

    def route(self, url_path: str, **kwargs):
        def register(view: Union[FUNC_BASED_VIEW, View]) -> Union[FUNC_BASED_VIEW, View]:
            nonlocal url_path, kwargs

            return self.__register(
                view,
                url_path,
                **kwargs,
            )
        return register

    def get(self, url_path: str, **kwargs):
        def register(view: Union[FUNC_BASED_VIEW, View]) -> Union[FUNC_BASED_VIEW, View]:
            nonlocal url_path, kwargs

            return self.__register_with_single_method(
                view,
                url_path,
                method='GET',
                **kwargs,
            )
        return register

    def post(self, url_path: str, **kwargs):
        def register(view: Union[FUNC_BASED_VIEW, View]) -> Union[FUNC_BASED_VIEW, View]:
            nonlocal url_path, kwargs

            return self.__register_with_single_method(
                view,
                url_path,
                method='POST',
                **kwargs,
            )
        return register

    def put(self, url_path: str, **kwargs):
        def register(view: Union[FUNC_BASED_VIEW, View]) -> Union[FUNC_BASED_VIEW, View]:
            nonlocal url_path, kwargs

            return self.__register_with_single_method(
                view,
                url_path,
                method='PUT',
                **kwargs,
            )
        return register

    def patch(self, url_path: str, **kwargs):
        def register(view: Union[FUNC_BASED_VIEW, View]) -> Union[FUNC_BASED_VIEW, View]:
            nonlocal url_path, kwargs

            return self.__register_with_single_method(
                view,
                url_path,
                method='PATCH',
                **kwargs,
            )
        return register

    def delete(self, url_path: str, **kwargs):
        def register(view: Union[FUNC_BASED_VIEW, View]) -> Union[FUNC_BASED_VIEW, View]:
            nonlocal url_path, kwargs

            return self.__register_with_single_method(
                view,
                url_path,
                method='DELETE',
                **kwargs,
            )
        return register

    def __str__(self) -> str:
        return f'Router(\n' \
               f'\tapp_name:\t"{self.app_name}"\n' \
               f'\turl_prefix:\t"{self.prefix}"\n' \
               f'\turls:\t\t{self.urls}\n' \
               f')'

    def __repr__(self) -> str:
        return str(self)
