# -*- coding: utf-8 -*-
from django.contrib import admin
from .inlines import NomineeInline, PlayerInline
from .models import Quiz, Category, Nominee, Player, Answer


class QuizAdmin(admin.ModelAdmin):
    inlines = [PlayerInline, ]


class CategoryAdmin(admin.ModelAdmin):
    inlines = [NomineeInline, ]
    list_display = ('name', 'quiz')
    list_filter = ('quiz', )


class NomineeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category', )


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz')
    list_filter = ('quiz', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('player', 'category', 'nominee')
    list_filter = ('player', 'category', )


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Nominee, NomineeAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Answer, AnswerAdmin)
