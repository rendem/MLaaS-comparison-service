from django import forms
from .models import Mlcmp
from django.http import HttpResponse
from django.conf import settings


class MlcmpForm(forms.ModelForm):
    class Meta:
        model = Mlcmp
        fields = ['image', 'result']
