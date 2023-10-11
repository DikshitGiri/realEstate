from django import forms
from .models import Property_type
class propertyType(forms.ModelForm):
    class Meta:
        model = Property_type
        fields = ['name']