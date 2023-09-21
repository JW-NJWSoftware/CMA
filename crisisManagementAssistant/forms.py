from django import forms
from crisisManagementAssistant.models import CMDoc


class CMDocForm(forms.ModelForm):
    class Meta:
        model = CMDoc
        fields = ('file', 'fileName',)
        widgets = {
            'fileName': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a name for your file',
                'class': 'form-control form-control-lg',
            }),
        }
