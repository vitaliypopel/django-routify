import uuid

from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from django_routify import (
    Router,

    ColonPattern,
    CurlyPattern,
    AnglePattern,
)

default_based_router = Router('<slug:TYPE>/')
colon_based_router = Router(':TYPE/', dynamic_pattern=ColonPattern)
curly_based_router = Router('{TYPE}/', dynamic_pattern=CurlyPattern)
angle_based_router = Router('<TYPE>/', dynamic_pattern=AnglePattern)


@default_based_router.route('books/<slug:book>/')
@colon_based_router.route('books/:book/')
@curly_based_router.route('books/{book}/')
@angle_based_router.route('books/<book>/')
def get_book(request: HttpRequest, TYPE: str, book: str) -> HttpResponse:
    return HttpResponse(
        f'TYPE: {TYPE}\n'
        f'Book "{book}"'
    )


@default_based_router.route('articles/<int:user_id>/<uuid:article_uuid>/')
@colon_based_router.route('articles/:user_id/:article_uuid/')
@curly_based_router.route('articles/{user_id}/{article_uuid}/')
@angle_based_router.route('articles/<user_id>/<article_uuid>/')
class ArticleView(View):
    async def get(
        self,
        request: HttpRequest,
        TYPE: str,
        user_id: int,
        article_uuid: uuid.UUID,
    ) -> HttpResponse:
        return HttpResponse(
            f'TYPE: {TYPE}'
            f'User ID: {user_id}\n'
            f'Article UUID: {article_uuid}'
        )
