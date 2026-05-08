from django.contrib.auth.mixins import UserPassesTestMixin


class RoleRequiredMixin(UserPassesTestMixin):

    role_name = None

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.is_authenticated and user.profile.role == self.role_name