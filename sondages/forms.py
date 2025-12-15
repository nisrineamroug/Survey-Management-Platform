from django import forms

class QuestionForm(forms.Form):
    text = forms.CharField(max_length=200, required=True)
    question_type = forms.ChoiceField(choices=[
        ('sc', 'Single Choice'),
        ('mc', 'Multiple Choice'),
        ('tx', 'Text'),
        ('scal', 'echelle (1-5)'),
    ], required=True)
    required = forms.BooleanField(required=False, initial=True)


class FilterForm(forms.Form):
    user = forms.CharField(required=False, label='User')
    date = forms.DateField(required=False, label='Date (YYYY-MM-DD)')


class SondageForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
