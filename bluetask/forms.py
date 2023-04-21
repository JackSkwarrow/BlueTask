from django import forms
from .models import SystemContract


class SystemContractForm(forms.ModelForm):
    class Meta:
        model = SystemContract
        fields = '__all__'
