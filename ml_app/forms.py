# ml_app/forms.py
from django import forms

class UploadCSVForm(forms.Form):
    file = forms.FileField(label='Subir archivo CSV', required=True)
