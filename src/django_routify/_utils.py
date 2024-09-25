from django.http import HttpRequest, HttpResponse

from typing import Callable, Any

FUNC_VIEW: type = Callable[[HttpRequest, ...], HttpResponse]


def validate_type(
        obj_name: str,
        obj: object,
        expected_type: type | tuple[Any, ...]
) -> None:
    '''
        Function validator for router class.
        Do not use it without need in your code!
        :param obj_name: str
        :param obj: object
        :param expected_type: type | tuple[Any, ...]
        :return: None
    '''

    if not isinstance(obj, expected_type):
        raise TypeError(
            f"Expected '{obj_name}' to be of type {expected_type}, "
            f"instead got {type(obj).__name__}"
        )
