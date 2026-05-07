from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied



class RoleRequiredMixin(AccessMixin):

    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            if request.user.profile.role != self.required_role:
                raise PermissionDenied("No Requiered Role")
        except AttributeError:
            raise PermissionDenied("No Required Role")
        return super().dispatch(request, *args, **kwargs)
