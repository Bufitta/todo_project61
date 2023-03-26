from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('user', 'done')
        widgets = {
            'deadline': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        # labels = {"text": "Текст", "group": "Группа"}
        help_texts = {
            'description': 'Опишите задачу как можно подробнее',
        }
        # error_messages = {}


class TaskFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, required=False)
