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
