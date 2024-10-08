import re
import uuid

from typing import Any
from ._abstraction import BasePattern


class Pattern(BasePattern):
    '''
    Pattern class is a default Pattern class

    Attributes:
        REGEX: str = r''
    '''

    REGEX = r''

    def normalize(
        self,
        custom_url: str,
        view: Any,
        class_based: bool,
    ) -> str:
        django_url = custom_url
        if self.REGEX == '':
            return django_url

        pass

    @staticmethod
    def _get_annotations(
        view: Any,
        class_based: bool,
    ) -> dict[str, type]:
        if class_based:
            if hasattr(view, 'parameters'):
                # getting annotations from attribute
                return view.parameters
            elif hasattr(view, 'get'):
                # getting annotations from params in GET method
                return view.get.__annotations__
            elif hasattr(view, 'post'):
                # getting annotations from params in POST method
                return view.post.__annotations__
            elif hasattr(view, 'put'):
                # getting annotations from params in PUT method
                return view.put.__annotations__
            elif hasattr(view, 'patch'):
                # getting annotations from params in PATCH method
                return view.patch.__annotations__
            elif hasattr(view, 'delete'):
                # getting annotations from params in DELETE method
                return view.delete.__annotations__
        else:
            # getting annotations from function params
            return view.__annotations__

    @staticmethod
    def _get_django_type(python_type: type) -> str:
        if python_type is int:
            return 'int'
        elif python_type is uuid.UUID:
            return 'uuid'
        return 'slug' # by default


class ColonPattern(Pattern):
    '''
    ColonPattern class for parsing colon based urls

    Example:
        /users/:id == /users/<int:id>
        articles/:article/ == articles/<slug:article>/

    Attributes:
        REGEX: str = r':(\w+)'
    '''

    REGEX = r':(\w+)'


class CurlyPattern(Pattern):
    '''
    CurlyPattern class for parsing curly brackets based urls

    Example:
        /users/{id} == /users/<int:id>
        articles/{article}/ == articles/<slug:article>/

    Attributes:
        REGEX: str = r'\{(\w+)\}'
    '''

    REGEX = r'\{(\w+)\}'


class AnglePattern(Pattern):
    '''
    AnglePattern class for parsing angle brackets based urls

    Example:
        /users/<id> == /users/<int:id>
        articles/<article>/ == articles/<slug:article>/

    Attributes:
        REGEX: str = r'<(\w+)>'
    '''

    REGEX = r'<(\w+)>'
