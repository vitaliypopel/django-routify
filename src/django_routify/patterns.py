import re
import uuid

from typing import Any, Dict, List, Type
from ._abstraction import BasePattern


class Pattern(BasePattern):
    r"""
    Pattern class is a default Pattern class

    Attributes:
        REGEX: str = ''
        DJANGO_REGEX = '<[a-zA-Z]+:([a-zA-Z]+)>'
    """

    REGEX = ''
    DJANGO_REGEX = r'<[a-zA-Z]+:([a-zA-Z]+)>'

    def normalize(
        self,
        custom_url: str,
        view: Any,
        class_based: bool,
    ) -> str:
        django_url = custom_url
        if self.REGEX == '' or not self.is_custom(custom_url):
            return django_url

        annotations = self._get_annotations(
            view=view, class_based=class_based,
        )

        url_params = self._get_url_params(custom_url)
        dynamic_params = self._get_dynamic_params(custom_url)

        for url_param, dynamic_param in zip(url_params, dynamic_params):
            python_type = annotations.get(url_param)
            django_type = self._get_django_type(python_type)

            django_url = django_url.replace(
                dynamic_param,
                f'<{django_type}:{url_param}>',
            )

        return django_url

    def _get_url_params(self, custom_url: str) -> List[str]:
        return re.findall(self.REGEX, custom_url)

    def _get_dynamic_params(self, custom_url: str) -> List[str]:
        return re.findall(
            self.REGEX.replace('(', '').replace(')', ''),
            custom_url,
        )

    def is_custom(self, url_: str) -> bool:
        is_custom = False

        params = re.findall(self.DJANGO_REGEX, url_)
        custom_params = self._get_url_params(url_)

        for custom_param in custom_params:
            if custom_param not in params:
                is_custom = True
                break

        return is_custom


    @staticmethod
    def _get_annotations(
        view: Any,
        class_based: bool,
    ) -> Dict[str, Type]:
        annotations = {}

        if class_based:
            if hasattr(view, 'parameters'):
                # getting annotations from attribute
                annotations =  view.parameters
            elif hasattr(view, 'get'):
                # getting annotations from params in GET method
                annotations =  view.get.__annotations__
            elif hasattr(view, 'post'):
                # getting annotations from params in POST method
                annotations =  view.post.__annotations__
            elif hasattr(view, 'put'):
                # getting annotations from params in PUT method
                annotations =  view.put.__annotations__
            elif hasattr(view, 'patch'):
                # getting annotations from params in PATCH method
                annotations =  view.patch.__annotations__
            elif hasattr(view, 'delete'):
                # getting annotations from params in DELETE method
                annotations =  view.delete.__annotations__
        else:
            # getting annotations from function params
            annotations =  view.__annotations__

        return annotations

    @staticmethod
    def _get_django_type(python_type: Type) -> str:
        if python_type is int:
            return 'int'
        elif python_type is uuid.UUID:
            return 'uuid'
        return 'slug' # by default

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(REGEX=r"{self.REGEX}")'

    def __repr__(self) -> str:
        return str(self)


class ColonPattern(Pattern):
    r"""
    ColonPattern class for parsing colon based urls

    Example:
        /users/:id == /users/<int:id>
        articles/:article/ == articles/<slug:article>/

    Attributes:
        REGEX: str = ':(\w+)'
        DJANGO_REGEX = '<[a-zA-Z]+:([a-zA-Z]+)>'
    """

    REGEX = r':(\w+)'


class CurlyPattern(Pattern):
    r"""
    CurlyPattern class for parsing curly brackets based urls

    Example:
        /users/{id} == /users/<int:id>
        articles/{article}/ == articles/<slug:article>/

    Attributes:
        REGEX: str = '\{(\w+)\}'
        DJANGO_REGEX = '<[a-zA-Z]+:([a-zA-Z]+)>'
    """

    REGEX = r'\{(\w+)\}'


class AnglePattern(Pattern):
    r"""
    AnglePattern class for parsing angle brackets based urls

    Example:
        /users/<id> == /users/<int:id>
        articles/<article>/ == articles/<slug:article>/

    Attributes:
        REGEX: str = '<(\w+)>'
        DJANGO_REGEX = '<[a-zA-Z]+:([a-zA-Z]+)>'
    """

    REGEX = r'<(\w+)>'
