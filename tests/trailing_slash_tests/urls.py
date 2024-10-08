from django_routify import include_router
from django.urls import path, include
from .views import (
    home,
    HomeRedirectView,
    HelloNameView,
    router_with_trailing,
    routify_without_trailing,
)

# Default Django's url registration with trailing slash
default_with_trailing_urlpatterns = [
    path(
        'test/', # url prefix '<host:port>/test/'
        include((
            [
                path('home/', home, name='home'),                                   # '<host:port>/test/home/'
                path('', HomeRedirectView.as_view(), name='home_redirect'),         # '<host:port>/test/'
                path('<slug:name>/', HelloNameView.as_view(), name='hello_name'),   # '<host:port>/test/<slug:name>/'
            ], # urlpatterns
            'test', # app_name
        ))
    ),
]


# Django Routify url registration with trailing slash
routify_with_trailing_urlpatterns = [
    include_router(router_with_trailing),
]


# Default Django's url registration with trailing slash
default_without_trailing_urlpatterns = [
    path(
        'test', # url prefix '<host:port>/test'
        include((
            [
                path('/home', home, name='home'),                                   # '<host:port>/test/home'
                path('', HomeRedirectView.as_view(), name='home_redirect'),         # '<host:port>/test'
                path('/<slug:name>', HelloNameView.as_view(), name='hello_name'),   # '<host:port>/test/<slug:name>'
            ], # urlpatterns
            'test', # app_name
        ))
    ),
]


# Django Routify url registration with trailing slash
routify_without_trailing_urlpatterns = [
    include_router(routify_without_trailing),
]
