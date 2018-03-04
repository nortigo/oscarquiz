# -*- coding: utf-8 -*-
from django.contrib.admin.options import StackedInline, TabularInline
from oscarquiz.models import Nominee, QuizPlayer


class QuizPlayerInline(TabularInline):
    model = QuizPlayer
    readonly_fields = ['score', ]
    extra = 0


class NomineeInline(StackedInline):
    model = Nominee
