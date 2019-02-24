# -*- coding: utf-8 -*-
from django import forms
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.forms import formset_factory, modelformset_factory
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

        category_count = len(CATEGORIES)
        answer_count = Answer.objects.filter(player=quiz_player.player).count()
        extra_field_count = category_count - answer_count

        AnswerFormset = modelformset_factory(
            Answer,
            exclude=[],
            form=AnswerForm,
            extra=extra_field_count,
            max_num=category_count
        )
        initial = []

        for category, _ in CATEGORIES:
            try:
                Answer.objects.get(
                    player=quiz_player.player,
                    category=category
                )
            except Answer.DoesNotExist:
                initial.append({
                    'player': quiz_player.player,
                    'category': category
                })

        formset = AnswerFormset(initial=initial)

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

        category_count = len(CATEGORIES)
        answer_count = Answer.objects.filter(player=quiz_player.player).count()
        extra_field_count = category_count - answer_count

        AnswerFormset = modelformset_factory(
            Answer,
            exclude=[],
            form=AnswerForm,
            extra=extra_field_count,
            max_num=category_count
        )
        initial = []

        for category, _ in CATEGORIES:
            try:
                Answer.objects.get(
                    player=quiz_player.player,
                    category=category
                )
            except Answer.DoesNotExist:
                initial.append({
                    'player': quiz_player.player,
                    'category': category
                })

        formset = AnswerFormset(initial=initial, data=request.POST)

        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            raise Exception

        return redirect(quiz_player.get_absolute_url())


class ResultsView(TemplateView):
    template_name = 'results.html'

    def get(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=kwargs['quiz_id'])

        return self.render_to_response(context={
            'categories': CATEGORIES,
            'quiz': quiz,
            'quiz_players': QuizPlayer.objects.filter(
                quiz=quiz
            ).order_by('quiz_id', 'player__name')
        })
