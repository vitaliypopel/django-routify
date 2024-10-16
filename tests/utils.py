from django.views.decorators.http import require_http_methods


def get_allowed_methods(view):
    """Helper function to get allowed methods for a view."""
    methods = []

    if callable(view):
        if hasattr(view, 'view_class'):
            for method in ['get', 'post', 'put', 'delete', 'patch']:
                if hasattr(view.view_class, method):
                    methods.append(method.upper())

        elif hasattr(view, 'decorator') and isinstance(view.decorator, require_http_methods):
            return view.decorator.methods

    elif hasattr(view, 'view_class'):
        for method in ['get', 'post', 'put', 'delete', 'patch']:
            if hasattr(view.view_class, method):
                methods.append(method.upper())

    return methods
