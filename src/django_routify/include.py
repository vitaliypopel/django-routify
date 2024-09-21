from django.urls import path, include, URLResolver

from .router import Router


def include_router(router: Router) -> URLResolver:
    '''
        Include router is a function that making include registered urls.
        Returning URLResolver which can be inserted into urlpatterns.
        :param router: Router
        :return: django.urls.URLResolver
    '''

    if not isinstance(router, Router):
        raise TypeError('Expected instance of django_routify.Router')

    return path(
        router.prefix,
        include((
            router.urls,
            router.app_name,
        ))
    )
