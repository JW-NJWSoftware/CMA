from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser
from django.contrib.auth import get_user_model, authenticate, login, logout

class AuthenticationViewTest(TestCase):
    def setUp(self):
        # Set up a client for making requests
        self.client = Client()
        self.user_data = {
            'username': 'genericuser',
            'email': 'example@example.com',
            'password': 'testpassword123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_registration(self):
        # Test user registration
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account created successfully')

        # Check if the user was created
        self.assertEqual(CustomUser.objects.filter(username='testuser').count(), 1)

    def test_login(self):
        # Test user registration
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account created successfully')

        # Check if the user was created
        self.assertEqual(CustomUser.objects.filter(username='testuser').count(), 1)

        # Test user login
        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }

        response = self.client.post(login_url, login_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check if the user is now authenticated
        user = authenticate(username='testuser', password='TestPassword123!')
        self.assertTrue(user.is_authenticated)
    
    def test_login_invalid_details(self):
        # Test user login
        login_url = reverse('login_view')
        login_data = {
            'username': 'genericuser',
            'password': 'TestPassword1234',
        }

        response = self.client.post(login_url, login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        self.client.login(username='genericuser', password='testpassword123')

        # Access the logout view with a POST request
        response = self.client.post("/auth/logout/", follow=True)

        # Check if the user is redirected to the home page (happens when logged out)
        self.assertRedirects(response, "/")

    def test_template_login(self):
        response = self.client.get("/auth/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
    
    def test_template_register(self):
        response = self.client.get("/auth/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")
    
    def test_template_logout(self):
        self.client.force_login(self.user)
        response = self.client.get("/auth/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/logout.html")

    def test_template_profile(self):
        self.client.force_login(self.user)
        response = self.client.get("/auth/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/profile.html")

    def test_template_settings(self):
        self.client.force_login(self.user)
        response = self.client.get("/auth/settings/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/settings.html")
    
    def test_logout_not_logged_in(self):
        response = self.client.get("/auth/logout/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_profile_not_logged_in(self):
        response = self.client.get("/auth/profile/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_settings_not_logged_in(self):
        response = self.client.get("/auth/settings/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
    
    def test_settings_view_no_settings(self):
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Log in the user with settings attribute
        self.client.login(username='testuser', password='TestPassword123!')

        # Access the settings view
        response = self.client.get(reverse('settings_view'))

        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)

        # Check if the default settings are used
        self.assertContains(response, 'value="16"')  # Default font size
        self.assertContains(response, 'value="1000"')  # Default chunk size
        self.assertContains(response, 'value="25.0"')  # Default sentence cut percentage
        self.assertContains(response, 'value="roberta-base-squad2"')  # Default modelChoice

    def test_settings_view_with_settings(self):
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Log in the user with settings attribute
        self.client.login(username='testuser', password='TestPassword123!')

        # Get the user instance created during registration
        user = CustomUser.objects.get(username='testuser')
        user.settings={
                'font_size': 18,
                'chunk_size': 1200,
                'sentence_cut_percentage': 30.0,
                'modelChoice': 'ensemble'
            }
        user.save()

        # Access the settings view
        response = self.client.get(reverse('settings_view'))

        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)

        # Check if the user's settings are displayed
        self.assertContains(response, 'value="18"')  # User's font size
        self.assertContains(response, 'value="1200"')  # User's chunk size
        self.assertContains(response, 'value="30.0"')  # User's sentence cut percentage
        self.assertContains(response, 'value="ensemble"')  

    def test_settings_update(self):
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        # Register the user
        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Get the user instance created during registration
        user = CustomUser.objects.get(username='testuser')

        # Log in the user
        self.client.login(username='testuser', password='TestPassword123!')

        # Set user's initial settings
        user.settings = {
            'font_size': 18,
            'chunk_size': 1200,
            'sentence_cut_percentage': 30.0,
            'modelChoice': 'ensemble'
        }
        user.save()

        # Access the settings view to update settings
        update_data = {
            'font_size': 20,
            'chunk_size': 1500,
            'sentence_cut_percentage': 40.0,
            'modelChoice': 'roberta-base-squad2'
        }

        response = self.client.post(reverse('settings_view'), update_data, follow=True)

        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)

        # Fetch the user again after update
        updated_user = CustomUser.objects.get(username='testuser')

        # Check if the user's settings are updated
        self.assertEqual(updated_user.settings['font_size'], 20)
        self.assertEqual(updated_user.settings['chunk_size'], 1500)
        self.assertEqual(updated_user.settings['sentence_cut_percentage'], 40.0)
        self.assertEqual(updated_user.settings['modelChoice'], 'roberta-base-squad2')

    def test_profile_view(self):
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        # Register the user
        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Log in the user
        self.client.login(username='testuser', password='TestPassword123!')

        # Access the profile view to check initial values
        response = self.client.get(reverse('profile_view'))

        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)

        # Check if the profile form is rendered with the correct initial values
        self.assertContains(response, 'value="testuser@example.com"')  # User's email

    def test_profile_view_update_profile(self):
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        # Register the user
        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Log in the user
        self.client.login(username='testuser', password='TestPassword123!')

        # Access the profile view to update profile
        update_data = {
            'update_profile': '',
            'email': 'updateduser@example.com',
        }

        response = self.client.post(reverse('profile_view'), update_data, follow=True)

        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)

        # Fetch the user again after update
        updated_user = CustomUser.objects.get(username='testuser')

        # Check if the user's profile is updated
        self.assertEqual(updated_user.email, 'updateduser@example.com')

    def test_profile_view_change_password(self):
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        # Register the user
        response = self.client.post(registration_url, registration_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Log in the user
        self.client.login(username='testuser', password='TestPassword123!')

        # Access the profile view to change password
        update_data = {
            'change_password': '',
            'old_password': 'TestPassword123!',
            'new_password1': 'NewPassword123!',
            'new_password2': 'NewPassword123!',
        }

        response = self.client.post(reverse('profile_view'), update_data, follow=True)

        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)

        # Fetch the user again after password change
        updated_user = CustomUser.objects.get(username='testuser')

        # Check if the user's password is updated
        self.assertTrue(updated_user.check_password('NewPassword123!'))