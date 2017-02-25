# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html
from oscarquiz.models import Answer, Category

register = template.Library()


@register.simple_tag
def display_answer(player, category):
    try:
        answer = Answer.objects.get(player=player, category=category)

        if not answer.nominee:
            return '-'

        if answer.nominee.is_winner is False:
            return answer.nominee.name

        return format_html(
            '{} <span class="glyphicon glyphicon-star text-success"></span>',
            answer.nominee.name)
    except Answer.DoesNotExist:
        return '-'


@register.simple_tag
def category_name(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return category.name
    except Category.DoesNotExist:
        return ''
