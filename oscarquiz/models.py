# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from oscarquiz.constants import CATEGORIES


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    expire_datetime = models.DateTimeField(null=True, blank=True)
    players = models.ManyToManyField('Player', through='QuizPlayer')

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name

    @property
    def is_past_due(self):
        return timezone.now() > self.expire_datetime


class Player(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class QuizPlayer(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4)
    quiz = models.ForeignKey(Quiz, related_name='quiz_qp', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='player_qp', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('quiz__name', 'player__name')
        unique_together = ('quiz', 'player')

    def __str__(self):
        return '{}: {}'.format(self.quiz, self.player)

    def get_absolute_url(self):
        return reverse('quiz', kwargs={
            'identifier': self.identifier,
        })


class Nominee(models.Model):
    oscar_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=255,
        choices=CATEGORIES
    )
    name = models.CharField(max_length=255)
    is_winner = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )
        unique_together = ('oscar_quiz', 'category', 'name')

    def __str__(self):
        return self.name

    @property
    def category_label(self):
        return dict(CATEGORIES)[self.category]


class Answer(models.Model):
    player = models.ForeignKey(
        Player,
        related_name='player_anwers',
        on_delete=models.CASCADE)
    category = models.CharField(
        max_length=255,
        choices=CATEGORIES
    )
    nominee = models.ForeignKey(
        Nominee,
        null=True, blank=True,
        related_name='nominee_answers',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('player__name', 'nominee__category')
        unique_together = ('player', 'category')

    def __str__(self):
        return '{}: {} ({})'.format(
            self.player.name,
            self.nominee.name if self.nominee else '-',
            self.category_label)

    @property
    def category_label(self):
        return dict(CATEGORIES)[self.category]
