from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import AnswerAdminForm
from .inlines import PlayerInline
from .models import Quiz, Nominee, Answer, Player
from .utils import admin_attr


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'expire_datetime', 'archived')
    inlines = (PlayerInline,)
    search_fields = ('name',)


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz', 'category', 'is_winner')
    list_filter = ('quiz', 'category', 'is_winner')
    autocomplete_fields = ('quiz',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:
            answer_queryset = Answer.objects

            for player in Player.objects.filter(quiz=obj.quiz).iterator():
                player.score = answer_queryset.filter(nominee__is_winner=True, player=player).count()
                player.save(update_fields=['score'])


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score')
    list_filter = ('quiz',)
    search_fields = ('user__last_name', 'user__first_name', 'quiz__name')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('player', 'get_category', 'nominee')
    list_filter = ('player', 'nominee__category')
    autocomplete_fields = ('player', 'nominee')
    form = AnswerAdminForm

    @admin_attr(_('Category'), 'category')
    def get_category(self, obj):
        return obj.category_label
