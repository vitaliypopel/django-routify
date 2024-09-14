from django.http import HttpRequest, HttpResponse
from django.views.generic import View, RedirectView
from django.shortcuts import reverse

from django_routify import Router

# Initializing new Router with needed settings
router = Router(
    prefix='/test',
    app_name='test',
    auto_trailing_slash=True
)


# Register home view function with auto_naming 'home' and with url 'home/'
@router.route('/home')
def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, World!')


# Register HomeRedirectView with auto_naming 'home_redirect' and with url ''
@router.route('/')
class HomeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('test:home')


# Register HelloWorldView with auto_naming 'hello_name' and with url '<slug:name>/'
@router.route('/<slug:name>')
class HelloNameView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        return HttpResponse(f'Hello, {name.capitalize()}!')
