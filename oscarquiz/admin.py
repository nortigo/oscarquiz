# -*- coding: utf-8 -*-
from django.contrib import admin
from oscarquiz.inlines import NomineeInline, PlayerInline
from oscarquiz.models import Quiz, Category, Nominee, Player, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [PlayerInline, ]
    list_display = ('name', 'expire_datetime')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [NomineeInline, ]
    list_display = ('name', 'quiz')
    list_filter = ('quiz', )


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'category', 'is_winner')
    list_filter = ('category', )

    def save_model(self, request, obj, form, change):
        super(NomineeAdmin, self).save_model(request, obj, form, change)

        for p in Player.objects.filter(quiz=obj.category.quiz):
            p.score = Answer.objects.filter(nominee__is_winner=True, player=p).count()
            p.save()


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz', 'score')
    list_filter = ('quiz', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('player', 'category', 'nominee')
    list_filter = ('player', 'category', )
