from django import forms
from .models import DeclareResult
from subjects.models import Subject  # Import the Subject model

class DeclareResultForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = DeclareResult
        fields = ['select_class', 'select_student', 'subjects']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].widget.attrs['class'] = 'form-control'
