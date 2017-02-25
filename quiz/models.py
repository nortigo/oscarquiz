# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Category(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='categories')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class NomineeType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Nominee(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    nominee_type = models.ForeignKey(NomineeType)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return '%s (%s)' % (self.name, self.category.name)


class Player(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz, related_name='players')


class Answer(models.Model):
    player = models.ForeignKey(Player, related_name='players')
