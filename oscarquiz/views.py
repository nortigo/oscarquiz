# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class QuizView(TemplateView):
    template_name = 'quiz.html'

    def get(self, request, *args, **kwargs):
        pass
