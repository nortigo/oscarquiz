from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .enums import Category


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    expire_datetime = models.DateTimeField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    def __str__(self):
        return self.name

    @property
    def is_past_due(self):
        return timezone.now() > self.expire_datetime


class Player(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='players', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('quiz', '-score', 'user__last_name', 'user__first_name')
        unique_together = ('quiz', 'user')
        verbose_name = _('Player')
        verbose_name_plural = _('Players')

    def __str__(self):
        return f'{self.quiz}: {self.name}'

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    @classmethod
    def update_score(cls, quiz):
        answer_queryset = Answer.objects
        for player in cls.objects.filter(quiz=quiz).iterator():
            player.score = answer_queryset.filter(nominee__is_winner=True, player=player).count()
            player.save(update_fields=['score'])


class Nominee(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='nominees', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=Category.choices)
    name = models.CharField(max_length=255)
    is_winner = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        unique_together = ('quiz', 'category', 'name')
        verbose_name = _('Nominee')
        verbose_name_plural = _('Nominees')

    def __str__(self):
        return f'{self.quiz} - {self.category_label}: {self.name}'

    @property
    def category_label(self):
        return Category(self.category).label


class Answer(models.Model):
    player = models.ForeignKey(Player, related_name='anwers', on_delete=models.CASCADE)
    nominee = models.ForeignKey(
        Nominee, null=True, blank=True, related_name='nominee_answers', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('player__user__last_name', 'player__user__first_name', 'nominee__category')
        unique_together = ('player', 'nominee')
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return f'{self.player.name}: {self.nominee_name} ({self.category_label})'

    @property
    def nominee_name(self):
        return self.nominee.name if self.nominee else '-'

    @property
    def category_label(self):
        return Category(self.nominee.category).label
