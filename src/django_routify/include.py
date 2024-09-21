from django.urls import path, include, URLResolver

from .router import Router


def include_router(router: Router) -> URLResolver:
    '''
        Include router is a function that making include registered urls.
        Returning list of path which can be inserted into urlpatterns.
        :param router: Router
        :return: django.urls.URLResolver
    '''
    return path(
        router.prefix,
        include((
            router.urls,
            router.app_name,
        ))
    )
