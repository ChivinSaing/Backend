"""Staff-only access for cafe portal pages (same rule as before)."""

from django.contrib.auth.decorators import user_passes_test

from polls.models import Staff


def staff_required(view_func):
    def _allowed(user):
        if not user.is_active:
            return False
        # Allow superusers to manage the portal even if no Staff row exists.
        if getattr(user, "is_superuser", False):
            return True
        # For normal portal staff, require a Staff record linked to this login user.
        return Staff.objects.filter(user=user, is_active=True).exists()

    return user_passes_test(
        _allowed,
        login_url="/login/",
    )(view_func)
