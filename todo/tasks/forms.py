from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('user', 'done')
        # labels = {'field_name': 'value'}
        help_texts = {'description': 'Введите подробное описание'}
        error_messages = {'title': {'max_length': 'Давай покороче!'}}
        widgets = {'deadline': forms.NumberInput(attrs={'type': 'date'})}


class TaskFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    priority = forms.ChoiceField(choices=[('', 'Все')] + Task.PRIORITY_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskFilterForm, self).__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(tasks__user=user).distinct()