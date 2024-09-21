from django_routify import include_router

from .views import router

urlpatterns = [
    include_router(router),
]
