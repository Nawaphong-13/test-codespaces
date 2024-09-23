# forms.py
from django import forms

class ImageForm(forms.ModelForm):
    class Meta:
        fields = ('file_original',)