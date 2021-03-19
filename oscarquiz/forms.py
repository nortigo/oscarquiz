from django import forms

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
