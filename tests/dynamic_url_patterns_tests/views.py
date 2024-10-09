import uuid
from audioop import reverse
from functools import reduce
from sys import prefix

from django.http import HttpRequest, HttpResponse
from django.views.generic import View, RedirectView

from django_routify import Router

default_based_router = Router('<slug:type>/')
colon_based_router = Router(':type/', ...)
curly_based_router = Router('{type}/', ...)
angle_based_router = Router('<type>/', ...)


@default_based_router.route('books/<slug:book>/')
@colon_based_router.route('books/:book/')
@curly_based_router.route('books/{book}/')
@angle_based_router.route('books/<book>/')
def get_book(request: HttpRequest, book: str) -> HttpResponse:
    return HttpResponse(f'Book "{book}"')


@default_based_router.route('articles/<int:user_id>/<uuid:article_uuid>/')
@colon_based_router.route('articles/:user_id/:article_uuid/')
@curly_based_router.route('articles/{user_id}/{article_uuid}/')
@angle_based_router.route('articles/<user_id>/<article_uuid>/')
class ArticleView(View):
    async def get(
        self,
        request: HttpRequest,
        user_id: int,
        article_uuid: uuid.UUID,
    ) -> HttpResponse:
        return HttpResponse(
            f'User ID: {user_id}\n'
            f'Article UUID: {article_uuid}'
        )


class RedirectToSomethingView(RedirectView):
    pass
