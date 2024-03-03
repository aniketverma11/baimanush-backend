from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtilsConfig(AppConfig):
    name = "baimanush_backend.utils"
    verbose_name = _("Utils")

    def ready(self):
        try:
            import qrcodeverification.users.signals 
        except ImportError:
            pass
