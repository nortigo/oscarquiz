# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    expire_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name

    @property
    def is_past_due(self):
        return timezone.now() > self.expire_datetime


class Category(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='categories')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def winners(self):
        return self.nominees.filter(is_winner=True)


class Nominee(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='nominees')
    is_winner = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, related_name='players')
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ('name', 'quiz__name')

    def __str__(self):
        return self.name


class Answer(models.Model):
    player = models.ForeignKey(Player, related_name='player_anwers')
    category = models.ForeignKey(Category, related_name='category_answers')
    nominee = models.ForeignKey(Nominee, null=True, blank=True, related_name='nominee_answers')

    class Meta:
        # unique_together = ('player', 'category')
        ordering = ('player__name', 'category__name')

    def __str__(self):
        return '%s: %s (%s)' % (
            self.player.name,
            self.nominee.name if self.nominee else '-',
            self.category.name)
