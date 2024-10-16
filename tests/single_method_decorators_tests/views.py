from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, reverse
from django.views.generic import View

from django_routify import Router, ColonPattern

router = Router(
    '/method',
    auto_trailing_slash=True,
    dynamic_pattern=ColonPattern,
)


@router.route('/redirect/:method', name='redirect', methods=['GET']) # same as @router.get
async def redirect_view(request: HttpRequest, method: str) -> HttpResponse:
    return redirect(f'method/{method}')


@router.get('/get')
class GetMethodView(View):
    async def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('GET method')


@router.post('/post')
class PostMethodView(View):
    async def post(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('POST method')


@router.put('/put')
class PutMethodView(View):
    async def put(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('PUT method')


@router.patch('/patch')
class PatchMethodView(View):
    async def patch(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('PATCH method')


@router.post('/delete')
class DeleteMethodView(View):
    async def delete(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('DELETE method')


@router.route('/all', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
class AllMethodsView(View):
    async def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('GET method')

    async def post(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('POST method')

    async def put(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('PUT method')

    async def patch(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('PATCH method')

    async def delete(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('DELETE method')
