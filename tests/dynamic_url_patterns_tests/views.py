import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import reverse
from django.views.generic import View, RedirectView

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


@default_based_router.route('books/<slug:book>/', name='book')
@colon_based_router.route('books/:book/', name='book')
@curly_based_router.route('books/{book}/', name='book')
@angle_based_router.route('books/<book>/', name='book')
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


@default_based_router.route('redirect/')
@colon_based_router.route('redirect/')
@curly_based_router.route('redirect/')
@angle_based_router.route('redirect/')
class RedirectToBookView(RedirectView):
    parameters = {
        'TYPE': str,
    }

    def get_redirect_url(self, *args, **kwargs) -> str:
        return reverse(viewname='book', args=('something', 'Alphabet',))
