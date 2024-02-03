from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.forms import UserCreateForm, AuthenticateForm, ProfileForm, SettingsForm, CustomPasswordChangeForm

class UserFormsTest(TestCase):

    def test_user_create_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
    
    def test_user_create_form_invalid_tos(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': False,
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_create_form_invalid_username(self):
        form_data = {
            'username': '',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_create_form_invalid_passwords(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data2 = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'wrongpassword',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form2 = UserCreateForm(data=form_data2)
        self.assertFalse(form2.is_valid())

    def test_user_create_form_invalid_email(self):
        # Test with invalid data, expect form not to be valid
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'password',
            'password2': 'differentpassword',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_authenticate_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save()
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        form = AuthenticateForm(data=form_data)
        self.assertTrue(form.is_valid())
        authenticated_user = form.get_user()
        self.assertEqual(authenticated_user, user)

    def test_authenticate_form_invalid_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save()
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        form = AuthenticateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_authenticate_form_no_user(self):
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        form = AuthenticateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save()
        form_data = {
            'first_name': 'UpdatedJohn',
            'last_name': 'UpdatedDoe',
            'email': 'updated@example.com',
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'UpdatedJohn')
    
    def test_profile_form_valid_same_info(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save()
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'testuser@example.com',
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'John')

    def test_profile_form_valid_single_field(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save()
        form_data = {
            'email': 'newtestuser@example.com',
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, 'newtestuser@example.com')

    def test_profile_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save()
        form_data = {
            'email': 'invalidemail',
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())

    def test_settings_form_valid(self):
        form_data = {
            'font_size':8,
            'chunk_size': 10,
            'sentence_cut_percentage': 0.5,
            'modelChoice': 'roberta-base-squad2',
        }
        form = SettingsForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['font_size'], 8)
        self.assertEqual(form.cleaned_data['chunk_size'], 10)
        self.assertEqual(form.cleaned_data['sentence_cut_percentage'], 0.5)
        self.assertEqual(form.cleaned_data['modelChoice'], 'roberta-base-squad2')

    def test_settings_form_invalid(self):
        # Test with invalid data, expect form not to be valid
        form_data = {
            'font_size':'not_an_integer',
            'chunk_size': 'not_an_integer',
            'sentence_cut_percentage': 'not_a_float',
            'modelChoice': 'invalid_choice',
        }
        form = SettingsForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_custom_password_change_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save(commit=False)
        form_data = {
            'old_password': 'testpassword123',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123',
        }
        form = CustomPasswordChangeForm(user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertTrue(updated_user.check_password('newtestpassword123'))

    def test_custom_password_change_form_invalid_passwords_different(self):
        # Test with invalid data, expect form not to be valid
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save(commit=False)
        form_data = {
            'old_password': 'testpassword123',
            'new_password1': 'newtestpassword123',
            'new_password2': 'differentpassword',
        }
        form = CustomPasswordChangeForm(user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_custom_password_change_form_invalid_wrong_password(self):
        # Test with invalid data, expect form not to be valid
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'ToS': True,
        }
        form = UserCreateForm(data=form_data)
        user = form.save(commit=False)
        form_data = {
            'old_password': 'wrongpassword',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123',
        }
        form = CustomPasswordChangeForm(user, data=form_data)
        self.assertFalse(form.is_valid())
