from functools import wraps
from django.shortcuts import redirect

#FIX THIS: https://www.geeksforgeeks.org/python/creating-custom-decorator-in-django-for-different-permissions/
def role_required(role_name):
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.role == role_name:
                return redirect("/accounts/login")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator