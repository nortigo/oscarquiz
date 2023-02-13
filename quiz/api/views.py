from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action

from .permissions import AdminHasWritePermission
from .serializers import (
    QuizSerializer,
    PlayerSerializer,
    CategoryNomineesSerializer,
    AnswerSerializer,
    NomineeSerializer,
)
from ..enums import Category
from ..models import Quiz, Answer, Player, Nominee


class QuizViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AdminHasWritePermission]

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

        diff = set(Category.values) - set(data.keys())

        for category in diff:
            data[category] = {
                'value': category,
                'label': Category(category).label,
                'nominees': [],
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

    def init_quiz(self, quiz_id):
        try:
            self.quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404()

    def create(self, request, *args, **kwargs):
        self.init_quiz(request.GET['qid'])
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        self.init_quiz(request.GET['qid'])
        return super().update(request, pk, *args, **kwargs)


class AnswerView(QuizMixin, APIView):
    def post(self, request, *args, **kwargs):
        self.init_quiz(request.data['quiz'])
        nominee = Nominee.objects.get(quiz=self.quiz, pk=request.data['nominee_id'])
        player = Player.objects.get(quiz=self.quiz, user=request.user)
        answer, created = Answer.objects.get_or_create(player=player, nominee=nominee)
        # Delete old answer from same category
        Answer.objects.filter(player=player, nominee__category=nominee.category).exclude(nominee=nominee).delete()
        serializer = AnswerSerializer(instance=answer, context={'request': request})
        return Response(serializer.data)


class NomineesView(QuizMixin, APIView):
    def post(self, request, *args, **kwargs):
        self.init_quiz(request.GET['qid'])
        serializers = []
        queryset = Nominee.objects
        category = request.GET['category']

        for data in request.data:
            try:
                instance = get_object_or_404(queryset, quiz=self.quiz, id=data['id'], category=category)
            except KeyError:
                instance = None
            serializer = NomineeSerializer(
                instance=instance, data={'quiz': self.quiz.pk, 'category': category, 'name': data['name']}
            )
            serializer.is_valid(raise_exception=True)
            # Skip save() here. We don't want to save all data if there is an error.
            serializers.append(serializer)

        for serializer in serializers:
            serializer.save()

        return Response([s.data for s in serializers])


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
        self.init_quiz(request.GET['qid'])
        instance: Nominee = self.get_object()
        instance.is_winner = True
        instance.save(update_fields=['is_winner'])
        Nominee.objects.filter(quiz=instance.quiz, category=instance.category).exclude(pk=instance.pk).update(
            is_winner=False
        )
        Player.update_score(quiz=self.quiz)
        serializer = NomineeSerializer(instance=instance)
        return Response(serializer.data)
