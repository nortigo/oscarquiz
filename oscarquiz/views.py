from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.forms import modelformset_factory

from .models import Quiz, QuizPlayer, Answer
from .forms import AnswerForm
from .constants import Category


class IndexView(ListView):
    template_name = 'index.html'
    model = Quiz


class QuizView(TemplateView):
    template_name = 'quiz.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        identifier = kwargs.get('identifier')

        quiz_player = get_object_or_404(QuizPlayer, identifier=identifier)

        if quiz_player.quiz.expire_datetime < timezone.now():
            return HttpResponseForbidden('No more answers allowed')

        player = quiz_player.player
        answer_queryset = Answer.objects
        category_count = len(Category)
        answer_count = answer_queryset.filter(player=player).count()
        extra_field_count = category_count - answer_count

        AnswerFormset = modelformset_factory(
            Answer, exclude=[], form=AnswerForm, extra=extra_field_count, max_num=category_count
        )
        initial = []

        for category in Category.values:
            try:
                answer_queryset.get(player=player, category=category)
            except Answer.DoesNotExist:
                initial.append({'player': player, 'category': category})

        formset = AnswerFormset(queryset=answer_queryset.filter(player=player), initial=initial)

        context['quiz'] = quiz_player.quiz
        context['answer_formset'] = formset
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        quiz_player = get_object_or_404(QuizPlayer, identifier=identifier)

        if quiz_player.quiz.is_past_due:
            return HttpResponseForbidden('No more answers allowed')

        player = quiz_player.player
        answer_queryset = Answer.objects
        category_count = len(Category)
        answer_count = answer_queryset.filter(player=player).count()
        extra_field_count = category_count - answer_count

        AnswerFormset = modelformset_factory(
            Answer, exclude=[], form=AnswerForm, extra=extra_field_count, max_num=category_count
        )
        initial = []

        for category in Category.values:
            try:
                answer_queryset.get(player=player, category=category)
            except Answer.DoesNotExist:
                initial.append({'player': player, 'category': category})

        formset = AnswerFormset(queryset=answer_queryset.filter(player=player), initial=initial, data=request.POST)

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
        queryset = QuizPlayer.objects.filter(quiz=quiz)
        ranking = queryset.values('player__name', 'score').order_by('-score')

        return self.render_to_response(
            context={
                'categories': Category.choices,
                'quiz': quiz,
                'ranking': ranking,
                'quiz_players': queryset.order_by('quiz_id', 'player__name'),
            }
        )
