from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.decorators import action

from .serializers import (
    QuizSerializer,
    PlayerSerializer,
    CategoryNomineesSerializer,
    AnswerSerializer,
)
from ..models import Quiz, Answer, Player


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


class AnswerViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(player__quiz=self.quiz)
        return queryset

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['quiz'] = self.quiz
        return context
