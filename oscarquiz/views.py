# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from .models import Quiz


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update({
            'quizzes': Quiz.objects.all()
        })
        return self.render_to_response(context=context)


class QuizView(TemplateView):
    template_name = 'quiz.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={
            'quiz': get_object_or_404(Quiz, id=kwargs['quiz_id'])
        })
