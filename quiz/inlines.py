from django.contrib.admin.options import StackedInline, TabularInline

from .models import Nominee, Player


class PlayerInline(TabularInline):
    model = Player
    readonly_fields = ('score',)
    autocomplete_fields = ('user',)
    extra = 0


class NomineeInline(StackedInline):
    model = Nominee
