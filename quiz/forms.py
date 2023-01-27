from django import forms
from django.utils.translation import gettext as _

from .models import Answer, Nominee


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = []
        widgets = {
            'player': forms.HiddenInput(),
            'category': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        try:
            category = kwargs['initial']['category']
        except KeyError:
            category = kwargs['instance'].category

        super().__init__(*args, **kwargs)
        self.fields['nominee'].queryset = Nominee.objects.filter(category=category)


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
