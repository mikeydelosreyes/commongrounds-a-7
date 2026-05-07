from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


def role_required(role):

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse_lazy("login"))
            try:
                if request.user.profile.role != role:
                    raise PermissionDenied("No Required Role")
            except AttributeError:
                raise PermissionDenied("No Required Role")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
