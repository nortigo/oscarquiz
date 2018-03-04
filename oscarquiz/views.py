# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.forms import formset_factory
from oscarquiz.models import Quiz, Player, Category, Answer
from oscarquiz.forms import AnswerForm


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

        if player.quiz.expire_datetime < timezone.now():
            return HttpResponseForbidden('No more answers allowed')

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

        if player.quiz.expire_datetime < timezone.now():
            return HttpResponseForbidden('No more answers allowed')

        AnswerFormset = formset_factory(AnswerForm, extra=0, max_num=Category.objects.all().count())
        initial = [{'player': player, 'category': category}
                   for category in player.quiz.categories.all()]

        formset = AnswerFormset(initial=initial, data=request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data['nominee']:
                    Answer.objects.update_or_create(
                        category=form.cleaned_data['category'],
                        player=form.cleaned_data['player'],
                        defaults={'nominee': form.cleaned_data['nominee']}
                    )

        return redirect(reverse('quiz', kwargs={
            'player_id': kwargs['player_id'],
            'quiz_id': kwargs['quiz_id']
        }))


class ResultsView(TemplateView):
    template_name = 'results.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={
            'quiz': get_object_or_404(Quiz, id=kwargs['quiz_id'])
        })
