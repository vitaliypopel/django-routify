from django.urls import path, include

from .router import Router


def include_router(router: Router) -> path:
    return path(router.prefix, include(router.urls))
