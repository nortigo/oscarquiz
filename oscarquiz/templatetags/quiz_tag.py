# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html
from oscarquiz.models import Answer, Category

register = template.Library()


@register.simple_tag
def display_answer(player, category):
    try:
        answer_qs = Answer.objects.select_related('player', 'category', 'nominee')
        answer_qs = answer_qs.get(player=player, category=category)

        if not answer_qs.nominee:
            return '-'

        if answer_qs.nominee.is_winner is False:
            name = answer_qs.nominee.name
            return name[:17] + '...' if len(name) > 20 else name

        return format_html(
            '<span class="glyphicon glyphicon-star text-success"></span> {}',
            answer_qs.nominee.name[:20])
    except Answer.DoesNotExist:
        return '-'


@register.simple_tag
def category_name(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return category.name
    except Category.DoesNotExist:
        return ''
