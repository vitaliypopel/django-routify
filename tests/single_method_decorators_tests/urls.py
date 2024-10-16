from django.urls import path, include

from django_routify import include_router

from .views import (
    router,

    redirect_view,
    GetMethodView,
    PostMethodView,
    PutMethodView,
    PatchMethodView,
    DeleteMethodView,
    AllMethodsView,
)


default_django_urlpatterns = [
    path(
        'method/', # URL prefix
        include(
            [
                path('redirect/<slug:method>/', redirect_view, name='redirect'), # redirect view
                path('get/', GetMethodView.as_view(), name='get_method'), # get method view
                path('post/', PostMethodView.as_view(), name='post_method'), # post method view
                path('put/', PutMethodView.as_view(), name='put_method'), # put method view
                path('patch/', PatchMethodView.as_view(), name='patch_method'), # patch method view
                path('delete/', DeleteMethodView.as_view(), name='delete_method'), # delete method view
                path('all/', AllMethodsView.as_view(), name='all_methods'), # all methods view
            ],
        ),
    ),
]

routify_urlpatterns = [
    include_router(router),
]
