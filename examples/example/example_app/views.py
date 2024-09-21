from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, RedirectView, FormView, View

from .forms import Form

from django_routify import Router

router = Router('example/', 'example_app')


@router.route('')
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('''
        <h2><ins>Index</ins> page</h2>
        <p>This is <b>index</b> view</p> 
    ''')


@router.route('async/', name='async')
async def async_view(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            'title': '__Async__ page',
            'content': 'This is **async** view',
        }
    )


@router.route('template/')
class GenericTemplateView(TemplateView):
    template_name = 'template.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(GenericTemplateView, self).get_context_data(**kwargs)
        context['view_name'] = 'Generic <ins>template</ins>'
        return context


@router.route('redirect/')
class GenericRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs) -> str:
        return reverse('example_app:generic_form')


@router.route('form/')
class GenericFormView(FormView):
    form_class = Form
    template_name = 'form.html'

    def form_valid(self, form: Form):
        return redirect(reverse(
            viewname='example_app:hello',
            args=(form.cleaned_data['name'],),
        ))


@router.route('<slug:name>/')
class HelloView(View):
    async def get(self, request: HttpRequest, name: str) -> HttpResponse:
        return HttpResponse(f'''
            <h2><ins>Hello</ins> page</h2>
            <p>Hello, <b>{name.capitalize()}</b>!</p>
        ''')
