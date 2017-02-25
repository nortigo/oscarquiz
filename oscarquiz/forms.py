# -*- coding: utf-8 -*-
from django import forms
from .models import Answer
from oscarquiz.models import Nominee


class AnswerForm(forms.ModelForm):
    nominee = forms.ModelChoiceField(queryset=Nominee.objects.none())

    class Meta:
        model = Answer
        exclude = []
        widgets = {
            'player': forms.HiddenInput(),
            'category': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        category = kwargs['initial']['category']
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['nominee'].queryset = Nominee.objects.filter(category=category)
