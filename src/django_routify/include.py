from django.urls import path, include

from .router import Router


def include_router(router: Router) -> list[path]:
    '''
        Include router is a function that making include registered urls.
        Returning list of path which can be inserted into urlpatterns.
        :param router: Router
        :return: list[django.urls.path]
    '''
    return path(
        router.prefix,
        include((
            router.urls,
            router.app_name,
        ))
    )
