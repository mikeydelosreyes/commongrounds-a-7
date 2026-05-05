from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class RoleRequiredMixin(AccessMixin):
    """Restrict CBV access to users whose Profile.role matches required_role.

    Usage:
        class ProductCreateView(RoleRequiredMixin, CreateView):
            required_role = "Market Seller"
    """
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            if request.user.profile.role != self.required_role:
                return redirect(reverse_lazy("accounts:permission_denied"))
        except AttributeError:
            return redirect(reverse_lazy("accounts:permission_denied"))
        return super().dispatch(request, *args, **kwargs)
