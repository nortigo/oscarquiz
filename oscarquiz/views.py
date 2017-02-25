# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.forms import formset_factory
from .models import Quiz, Player
from .forms import AnswerForm
from oscarquiz.models import Category


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
        player = get_object_or_404(Player, id=kwargs['player_id'], quiz_id=kwargs['quiz_id'])
        AnswerFormset = formset_factory(AnswerForm, extra=0, max_num=Category.objects.all().count())
        formset = AnswerFormset(initial=[{'player': player, 'category': c}
                                         for c in player.quiz.categories.all()])

        return self.render_to_response(context={
            'quiz': player.quiz,
            'answer_formset': formset,
            'player_id': kwargs['player_id'],
            'quiz_id': kwargs['quiz_id'],
        })

    def post(self, request, *args, **kwargs):
        player = get_object_or_404(Player, id=kwargs['player_id'], quiz_id=kwargs['quiz_id'])
        AnswerFormset = formset_factory(AnswerForm, extra=0, max_num=Category.objects.all().count())
        formset = AnswerFormset(initial=[{'player': player, 'category': c}
                                         for c in player.quiz.categories.all()],
                                data=request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data['nominee']:
                    form.save()

        return self.render_to_response(context={
            'quiz': player.quiz,
            'answer_formset': formset,
            'player_id': kwargs['player_id'],
            'quiz_id': kwargs['quiz_id'],
        })


class ResultsView(TemplateView):
    template_name = 'results.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={
            'quiz': get_object_or_404(Quiz, id=kwargs['quiz_id'])
        })
