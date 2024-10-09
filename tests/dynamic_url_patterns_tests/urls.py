from django_routify import include_router
from django.urls import path, include
from .views import (
    get_book,
    ArticleView,
    RedirectToBookView,

    default_based_router,
    colon_based_router,
    curly_based_router,
    angle_based_router,
)

# Default Django's url registration
default_urlpatterns = [
    path('<slug:TYPE>/', # prefix for each url
        include(
            [
                path('books/<slug:book>/', get_book, name='book'),
                path('articles/<int:user_id>/<uuid:article_uuid>/',
                     ArticleView.as_view(), name='article'),
                path('redirect/',
                     RedirectToBookView.as_view(), name='redirect_to_book'),
            ],
        ),
    ),
]

# Default based router urls
default_based_urlpatterns = [
    include_router(default_based_router),
]

# Colon based router urls
colon_based_urlpatterns = [
    include_router(colon_based_router),
]

# Curly based router urls
curly_based_urlpatterns = [
    include_router(curly_based_router),
]

# Angle based router urls
angle_based_urlpatterns = [
    include_router(angle_based_router),
]
