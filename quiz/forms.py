from django import forms
from django.utils.translation import gettext as _

from .models import Answer


class AnswerAdminForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = []

    def clean(self):
        cleaned_data = super().clean()
        player = cleaned_data['player']
        nominee = cleaned_data.get('nominee')
        if nominee and nominee.quiz != player.quiz:
            self.add_error('nominee', _('Please select nominee from same quiz.'))
        return cleaned_data
