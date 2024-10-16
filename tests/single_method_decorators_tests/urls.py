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


