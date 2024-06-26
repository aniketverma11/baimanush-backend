from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from utils.behaviours import UUIDMixin, MobileMixin


class User(AbstractUser, UUIDMixin, MobileMixin):
    """
    Default custom user model .
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
