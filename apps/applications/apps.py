from cProfile import label
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApplicationsConfig(AppConfig):
    name = "apps.applications"
    verbose_name = _("Applications")

    def ready(self):
        try:
            import apps.applications.signals  # noqa F401
        except ImportError:
            pass
