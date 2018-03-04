# -*- coding: utf-8 -*-
from django import forms
from oscarquiz.constants import CATEGORIES
from oscarquiz.models import Answer, Nominee


class AnswerForm(forms.ModelForm):
    nominee = forms.ModelChoiceField(queryset=Nominee.objects.none(), required=False)
    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Answer
        exclude = []
        widgets = {
            'player': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        player = kwargs['initial']['player']
        category = kwargs['initial']['category']

        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['nominee'].queryset = Nominee.objects.filter(category=category)

        try:
            answer = Answer.objects.get(player=player, nominee__category=category)

            if answer.nominee:
                self.fields['nominee'].initial = answer.nominee
        except Answer.DoesNotExist:
            pass
