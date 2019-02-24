# -*- coding: utf-8 -*-
from django.contrib import admin
from oscarquiz.inlines import QuizPlayerInline
from oscarquiz.models import Quiz, Player, Nominee, Answer, QuizPlayer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizPlayerInline, ]
    list_display = ('name', 'expire_datetime')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('name', 'oscar_quiz', 'category', 'is_winner')
    list_filter = ('oscar_quiz', 'category', 'is_winner')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        answer_queryset = Answer.objects

        for qp in QuizPlayer.objects.filter(quiz=obj.oscar_quiz):
            qp.score = answer_queryset.filter(
                nominee__is_winner=True,
                player=qp.player
            ).count()
            qp.save()


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('player', 'get_category', 'nominee')
    list_filter = ('player', 'category')

    def get_category(self, obj):
        return obj.category_label
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category'
