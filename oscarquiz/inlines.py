# -*- coding: utf-8 -*-
from django.contrib.admin.options import StackedInline
from oscarquiz.models import Nominee, Player


class PlayerInline(StackedInline):
    model = Player


class NomineeInline(StackedInline):
    model = Nominee
