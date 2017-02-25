# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html
from oscarquiz.models import Answer

register = template.Library()


@register.simple_tag
def display_answer(player, category):
    try:
        answer = Answer.objects.get(player=player, category=category)
        if answer.nominee.is_winner:
            return format_html(
                '{} <span class="glyphicon glyphicon-star text-success"></span>',
                answer.nominee.name)
        else:
            return answer.nominee.name
    except Answer.DoesNotExist:
        return '-'
