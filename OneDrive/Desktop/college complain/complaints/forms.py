from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Short title of your complaint'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your complaint in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }