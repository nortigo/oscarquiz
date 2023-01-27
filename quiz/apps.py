from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuizConfig(AppConfig):
    name = 'quiz'
    verbose_name = _('Oscar Quiz')
