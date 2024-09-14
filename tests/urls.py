# Default Django's url registration
from django.urls import path, include
from .views import home, HomeRedirectView, HelloNameView

default_urlpatterns = [
    path(
        'test/', # url prefix
        include((
            [
                path('home/', home, name='home'),
                path('', HomeRedirectView.as_view(), name='home_redirect'),
                path('<slug:name>/', HelloNameView.as_view(), name='hello_name'),
            ], # urlpatterns
            'test', # app_name
        ))
    ),
]


# Django Routify url registration
from django_routify import include_router
from .views import router

routify_urlpatterns = [
    include_router(router),
]
