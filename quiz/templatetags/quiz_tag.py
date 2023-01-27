from django import template
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html
from ..enums import Category
from ..models import Answer

register = template.Library()


@register.simple_tag
def display_answer(player, category):
    try:
        answer_qs = Answer.objects.select_related('player', 'nominee').get(player=player, nominee__category=category)

        if not answer_qs.nominee:
            return '-'

        if not answer_qs.nominee.is_winner:
            name = answer_qs.nominee.name
            return truncatechars(name, 20)

        return format_html(
            '<span class="glyphicon glyphicon-star text-success"></span> {}', answer_qs.nominee.name[:20]
        )
    except Answer.DoesNotExist:
        return '-'


@register.simple_tag
def category_name(category):
    try:
        return Category[category].label
    except KeyError:
        return ''
