from typing import Any, Tuple


def _validate_type(
    obj_name: str,
    obj: object,
    expected_type: type | Tuple[Any, ...],
) -> None:
    """
    Function validator for router class.
    Do not use it without need in your code!
    :param obj_name: str
    :param obj: object
    :param expected_type: type | Tuple[Any, ...]
    :return: None
    """

    if not isinstance(obj, expected_type):
        raise TypeError(
            f'Expected "{obj_name}" to be of type {expected_type}, '
            f'instead got {type(obj).__name__}'
        )
