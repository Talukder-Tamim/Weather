from django.forms import ModelForm, TextInput
from .models import State

class StateForm(ModelForm):
    class Meta:
        model = State
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City name'})}
