from django.http import HttpRequest, HttpResponse
from django.views.generic import View, RedirectView
from django.shortcuts import reverse

from django_routify import Router

# Initializing new Router with needed settings
router_with_trailing = Router(
    prefix='/test',     # <host:port>/test/
    app_name='test',
    auto_trailing_slash=True,
    # auto_trailing_slash will remove not needed slashes
    # before and after url_path and prefix,
    # and will add slash to the end
)

routify_without_trailing = Router(
    prefix='/test',     # <host:port>/test
    app_name='test',
    # auto_trailing_slash by default equal False
)


# Register home view function with auto_naming 'home'
@router_with_trailing.route('/home')        # <host:port>/test/home/
@routify_without_trailing.route('/home')    # <host:port>/test/home
def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello, World!')


# Register HomeRedirectView with auto_naming 'home_redirect'
@router_with_trailing.route('/')        # <host:port>/test/
@routify_without_trailing.route('')    # <host:port>/test
class HomeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('test:home')


# Register HelloWorldView with auto_naming 'hello_name'
@router_with_trailing.route('/<slug:name>')        # <host:port>/test/<slug:name>/
@routify_without_trailing.route('/<slug:name>')    # <host:port>/test/<slug:name>
class HelloNameView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        return HttpResponse(f'Hello, {name.capitalize()}!')
