from django import forms
from .models import Task, List

class TaskForm(forms.ModelForm):
    list = forms.ModelChoiceField(queryset=List.objects.all(), required=False)
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y']
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'list']