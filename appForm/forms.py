from django import forms
from appForm.models import Cep

class FormCep(forms.ModelForm):
    class Meta:
        model = Cep
        fields = ('cep',)

        widgets = {
            'cep': forms.TextInput(attrs={'class': 'form-control border border-success', 'placeholder': 'Seu CEP aqui'}),
        }

        labels = {
            'cep' : ''
        }
        