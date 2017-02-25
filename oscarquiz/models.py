# -*- coding: utf-8 -*-
from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name


class Category(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='categories')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Nominee(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, related_name='players')

    class Meta:
        ordering = ('name', 'quiz__name')

    def __str__(self):
        return self.name


class Answer(models.Model):
    player = models.ForeignKey(Player, related_name='player_anwers')
    category = models.ForeignKey(Category, related_name='category_answers')
    nominee = models.ForeignKey(Nominee, related_name='nominee_answers')

    class Meta:
        unique_together = ('player', 'category')
        ordering = ('player__name', 'category__name')

    def __str__(self):
        return '%s: %s (%s)' % (
            self.player.name,
            self.nominee.name,
            self.category.name)
