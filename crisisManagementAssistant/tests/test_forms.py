from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from crisisManagementAssistant.forms import CMDocForm
from crisisManagementAssistant.models import CMDoc

class CMDocFormTest(TestCase):

    def test_cmdoc_form_valid(self):
        form_data = {
            'fileName': 'ValidFile',
            'desc': 'Valid Description',
        }
        file_data = {
            'file': SimpleUploadedFile("test_file.txt", b"file_content"),
        }
        form = CMDocForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())
    
    def test_cmdoc_form_valid_without_desc(self):
        form_data = {
            'fileName': 'ValidFile',
            'desc': '',
        }
        file_data = {
            'file': SimpleUploadedFile("test_file.txt", b"file_content"),
        }
        form = CMDocForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_cmdoc_form_invalid_fileName(self):
        # Test with invalid data, expect form not to be valid
        form_data = {
            'fileName': '',
            'desc': 'Valid Description',
        }
        file_data = {
            'file': SimpleUploadedFile("test_file.txt", b"file_content"),
        }
        form = CMDocForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())

    def test_cmdoc_form_missing_file(self):
        # Test when the file field is missing, expect form not to be valid
        form_data = {
            'fileName': 'ValidFile',
            'desc': 'Valid Description',
        }
        form = CMDocForm(data=form_data, files={})
        self.assertFalse(form.is_valid())

    def test_cmdoc_form_widgets(self):
        # Test whether form fields have the correct widgets
        form = CMDocForm()
        self.assertIsInstance(form.fields['fileName'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['desc'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['file'].widget, forms.FileInput)

