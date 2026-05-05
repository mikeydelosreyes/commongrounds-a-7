from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse_lazy


def role_required(role):
    """Restrict FBV access to users whose Profile.role matches role.

    Usage:
        @role_required("Market Seller")
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse_lazy("login"))
            try:
                if request.user.profile.role != role:
                    return redirect(reverse_lazy("accounts:permission_denied"))
            except AttributeError:
                return redirect(reverse_lazy("accounts:permission_denied"))
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
