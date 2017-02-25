# -*- coding: utf-8 -*-
from django.contrib.admin.options import StackedInline
from .models import Nominee
from oscarquiz.models import Player


class PlayerInline(StackedInline):
    model = Player


class NomineeInline(StackedInline):
    model = Nominee
