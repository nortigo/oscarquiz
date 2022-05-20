from django.contrib.admin.options import StackedInline, TabularInline

from .models import Nominee, QuizPlayer


class QuizPlayerInline(TabularInline):
    model = QuizPlayer
    readonly_fields = [
        'score',
    ]
    extra = 0


class NomineeInline(StackedInline):
    model = Nominee
