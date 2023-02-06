from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action

from .serializers import (
    QuizSerializer,
    PlayerSerializer,
    CategoryNomineesSerializer,
    AnswerSerializer,
    NomineeSerializer,
)
from ..models import Quiz, Answer, Player, Nominee


class QuizViewSet(ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        quiz = get_object_or_404(Quiz.objects.all(), pk=pk)
        serializer = PlayerSerializer(quiz.players.all(), many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def nominees(self, request, pk=None):
        quiz = get_object_or_404(Quiz.objects.all(), pk=pk)

        data = {}
        for nominee in quiz.nominees.all():
            try:
                data[nominee.category]['nominees'].append(nominee)
            except KeyError:
                data[nominee.category] = {
                    'value': nominee.category,
                    'label': nominee.category_label,
                    'nominees': [nominee],
                }

        serializer = CategoryNomineesSerializer(data.values(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        quiz = get_object_or_404(Quiz.objects.all(), pk=pk)
        serializer = AnswerSerializer(
            Answer.objects.filter(player__quiz=quiz, player__user=request.user), many=True, context={'request': request}
        )
        return Response(serializer.data)


class QuizMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = None

    def init_quiz(self, request):
        try:
            self.quiz = Quiz.objects.get(pk=self.request.GET['qid'])
        except (KeyError, Quiz.DoesNotExist):
            raise Http404()

    def create(self, request, *args, **kwargs):
        self.init_quiz(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        self.init_quiz(request)
        return super().update(request, pk, *args, **kwargs)


class AnswerViewSet(QuizMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(player__quiz=self.quiz)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['quiz'] = self.quiz
        return context


class NomineeViewSet(QuizMixin, GenericViewSet):
    permission_classes = [IsAdminUser]
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(quiz=self.quiz)
        return queryset

    @action(detail=True, methods=['patch'])
    def winner(self, request, pk=None):
        self.init_quiz(request)
        instance: Nominee = self.get_object()
        instance.is_winner = True
        instance.save(update_fields=['is_winner'])
        Nominee.objects.filter(quiz=instance.quiz, category=instance.category).exclude(pk=instance.pk).update(
            is_winner=False
        )
        Player.update_score(quiz=self.quiz)
        serializer = NomineeSerializer(instance=instance)
        return Response(serializer.data)
