# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.forms import formset_factory
from oscarquiz.models import Quiz, QuizPlayer, Answer
from oscarquiz.forms import AnswerForm
from oscarquiz.constants import CATEGORIES


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['quizzes'] = Quiz.objects.all()
        return self.render_to_response(context=context)


class QuizView(TemplateView):
    template_name = 'quiz.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        identifier = kwargs.get('identifier')

        quiz_player = get_object_or_404(
            QuizPlayer,
            identifier=identifier)

        if quiz_player.quiz.expire_datetime < timezone.now():
            return HttpResponseForbidden('No more answers allowed')

        AnswerFormset = formset_factory(AnswerForm, extra=0, max_num=len(CATEGORIES))
        formset = AnswerFormset(initial=[{'player': quiz_player.player, 'category': category}
                                         for category, _ in CATEGORIES])

        context['quiz'] = quiz_player.quiz
        context['answer_formset'] = formset
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        quiz_player = get_object_or_404(
            QuizPlayer,
            identifier=identifier)

        if quiz_player.quiz.is_past_due:
            return HttpResponseForbidden('No more answers allowed')

        AnswerFormset = formset_factory(AnswerForm, extra=0, max_num=len(CATEGORIES))
        initial = [{'player': quiz_player.player, 'category': category}
                   for category, _ in CATEGORIES]

        formset = AnswerFormset(initial=initial, data=request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data['nominee']:
                    Answer.objects.update_or_create(
                        player=form.cleaned_data['player'],
                        defaults={'nominee': form.cleaned_data['nominee']}
                    )
        else:
            print(formset.errors)
            raise Exception

        return redirect(quiz_player.get_absolute_url())


class ResultsView(TemplateView):
    template_name = 'results.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={
            'categories': CATEGORIES,
            'quiz_players': QuizPlayer.objects.filter(
                quiz=get_object_or_404(Quiz, id=kwargs['quiz_id'])
            ).order_by('quiz_id', 'player__name')
        })
