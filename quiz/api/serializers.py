from rest_framework.fields import SerializerMethodField, CharField, IntegerField, empty
from rest_framework.serializers import ModelSerializer, Serializer

from ..models import Quiz, Player, Nominee, Answer


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'expire_datetime', 'archived']


class PlayerSerializer(ModelSerializer):
    can_play = SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'score', 'user_id', 'can_play']
        extra_kwargs = {'name': {'read_only': True}}

    def get_can_play(self, obj):
        user = self.context['request'].user
        return user == obj.user and not obj.quiz.is_past_due


class NomineeSerializer(ModelSerializer):
    class Meta:
        model = Nominee
        fields = ['id', 'name', 'is_winner', 'quiz', 'category']
        extra_kwargs = {'quiz': {'write_only': True}, 'category': {'write_only': True}}


class CategoryNomineesSerializer(Serializer):
    value = CharField(max_length=50, read_only=True)
    label = CharField(max_length=150, read_only=True)
    nominees = NomineeSerializer(many=True)


class AnswerSerializer(ModelSerializer):
    player = PlayerSerializer(read_only=True)
    nominee = NomineeSerializer(read_only=True)
    nominee_id = IntegerField(write_only=True)
    category = SerializerMethodField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'player', 'nominee', 'nominee_id', 'category']

    def get_category(self, obj: Answer):
        return obj.nominee.category

    def save(self, **kwargs):
        return super().save(player=self.get_player())

    def get_player(self):
        return Player.objects.get(user=self.context['request'].user, quiz=self.context['quiz'])
