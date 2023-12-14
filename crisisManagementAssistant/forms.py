from django import forms
from crisisManagementAssistant.models import CMDoc


class CMDocForm(forms.ModelForm):
    class Meta:
        model = CMDoc
        fields = ('fileName', 'desc', 'file')
        widgets = {
            'fileName': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a name for your file',
                'class': 'form-control form-control-lg',
            }),
                        'desc': forms.Textarea(attrs={
                'placeholder': 'Enter a description',
                'class': 'form-control',
                'rows': 3,
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
        }
