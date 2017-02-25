# -*- coding: utf-8 -*-
from django import forms
from .models import Answer
from oscarquiz.models import Nominee


class AnswerForm(forms.ModelForm):
    nominee = forms.ModelChoiceField(queryset=Nominee.objects.none(), required=False)

    class Meta:
        model = Answer
        exclude = []
        widgets = {
            'player': forms.HiddenInput(),
            'category': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        player = kwargs['initial']['player']
        category = kwargs['initial']['category']

        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['nominee'].queryset = Nominee.objects.filter(category=category)

        try:
            answer = Answer.objects.get(player=player, category=category)

            if answer.nominee:
                self.fields['nominee'].initial = answer.nominee
        except Answer.DoesNotExist:
            pass
