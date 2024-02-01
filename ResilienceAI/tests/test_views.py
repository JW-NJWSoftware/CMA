from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser
from django.contrib.auth import get_user_model, login
from django.core.files.uploadedfile import SimpleUploadedFile

class ResilienceAIViewTest(TestCase):
    def setUp(self):
        # Set up a client for making requests
        self.client = Client()
        self.user_data = {
            'username': 'genericuser',
            'email': 'example@example.com',
            'password': 'testpassword123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_guides(self):
        self.client.force_login(self.user)
        response = self.client.get("/guides/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "guides.html")
    
    def test_guides_logged_out(self):
        response = self.client.get("/guides/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
    
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_search(self):
        # Register user
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        response = self.client.post(registration_url, registration_data)

        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }

        response = self.client.post(login_url, login_data)

        self.dummy_file = SimpleUploadedFile("dummy.txt", b"Dummy file content.")

        fileData = {
            'switch_value':'off',
            'file': self.dummy_file,
            'fileName':'testFile'
        }

        chatData = {
            'chat_name': 'testChat'
        }

        self.client.post(reverse('upload_file'), fileData)
        self.client.get(reverse('new_chat'), chatData)

        response_search = self.client.get("/search/", {'search_value':'test'})

        self.assertEqual(response_search.status_code, 200)
        self.assertTemplateUsed(response_search, "search.html")
        self.assertContains(response_search, 'testFile')
        self.assertContains(response_search, 'testChat')

        response_search = self.client.get("/search/", {'search_value':'Chat'})

        self.assertEqual(response_search.status_code, 200)
        self.assertTemplateUsed(response_search, "search.html")
        self.assertNotContains(response_search, 'testFile')
        self.assertContains(response_search, 'testChat')

        response_search = self.client.get("/search/", {'search_value':''})

        self.assertEqual(response_search.status_code, 200)
        self.assertTemplateUsed(response_search, "search.html")
        self.assertContains(response_search, 'No search value provided.')

        self.dummy_file.close()
    
    def test_search_group_files(self):
        # Register user
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        registration_data_2 = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        self.client.post(registration_url, registration_data)
        self.client.post(registration_url, registration_data_2)

        login_url = reverse('login_view')
        logout_url = reverse('logout_view')
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }
        login_data_2 = {
            'username': 'testuser2',
            'password': 'TestPassword123!',
        }

        self.client.post(login_url, login_data)

        self.dummy_file = SimpleUploadedFile("dummy.txt", b"Dummy file content.")

        fileData = {
            'switch_value':'off',
            'file': self.dummy_file,
            'fileName':'testFile'
        }

        chatData = {
            'chat_name': 'testChat'
        }

        self.client.post(reverse('upload_file'), fileData)
        self.client.get(reverse('new_chat'), chatData)

        self.client.post("/auth/logout/")
        self.client.post(login_url, login_data_2)

        #add both users to a group
        user1 = CustomUser.objects.get(username='testuser')
        user1.group = 'test'
        user1.save()
        user1.role='owner'
        user1.save()
        user2 = CustomUser.objects.get(username='testuser2')
        user2.group = 'test'
        user2.save()
        user2.role='member'
        user2.save()

        response_search = self.client.get("/search/", {'search_value':'test'})

        self.assertEqual(response_search.status_code, 200)
        self.assertTemplateUsed(response_search, "search.html")
        self.assertContains(response_search, 'testFile')
        self.assertContains(response_search, 'testChat')

        self.dummy_file.close()

