from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser
from crisisManagementAssistant.models import CMDoc, Chat
from django.contrib.auth import get_user_model, login
from django.core.files.uploadedfile import SimpleUploadedFile

class ManageViewsTest(TestCase):
    def setUp(self):
        # Set up a client for making requests
        self.client = Client()

        # Register user
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        self.client.post(registration_url, registration_data)

        #login to account
        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }

        self.client.post(login_url, login_data)

    def test_manage_no_group(self):
        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'Create group')
    
    def test_manage_group(self):
        user1 = CustomUser.objects.get(username='testuser')
        user1.group = 'test'
        user1.save()
        user1.role='owner'
        user1.save()

        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertNotContains(response, 'Create group')
    
    def test_view_other_group_members(self):
        user = CustomUser.objects.get(username='testuser')
        user.group = 'test'
        user.save()
        user.role='owner'
        user.save()

        C2 = Client()
        C3 = Client()

        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C2.post(registration_url, registration_data)

        registration_data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C3.post(registration_url, registration_data)

        user = CustomUser.objects.get(username='testuser3')
        user.group = 'test'
        user.save()
        user.role='member'
        user.save()

        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'testuser3')
        self.assertNotContains(response, 'testuser2')
    
    def test_remove_from_group_not_owner(self):
        user = CustomUser.objects.get(username='testuser')
        user.group = 'test'
        user.save()
        user.role='member'
        user.save()

        C = Client()

        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C.post(registration_url, registration_data)

        user = CustomUser.objects.get(username='testuser2')
        user.group = 'test'
        user.save()
        user.role='member'
        user.save()

        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'testuser2')

        response = self.client.get(reverse('remove_from_group'), {'user_email':'testuser2@example.com'}, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_remove_from_group(self):
        user = CustomUser.objects.get(username='testuser')
        user.group = 'test'
        user.save()
        user.role='Owner'
        user.save()

        C = Client()

        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C.post(registration_url, registration_data)

        user = CustomUser.objects.get(username='testuser2')
        user.group = 'test'
        user.save()
        user.role='member'
        user.save()

        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'testuser2')

        response = self.client.get(reverse('remove_from_group'), {'user_email':'testuser2@example.com'}, follow=True)
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertNotContains(response, 'testuser2')
    
    def test_invite_send(self):
        C = Client()

        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C.post(registration_url, registration_data)

        user = CustomUser.objects.get(username='testuser2')
        user.group = 'test'
        user.save()
        user.role='Owner'
        user.save()

        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser2',
            'password': 'TestPassword123!',
        }

        C.post(login_url, login_data)
        C.get(reverse('add_to_group'), {'user_email':'testuser@example.com'})
        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'You have been invited to the "test" group.')
    
    def test_invite_accept(self):
        C = Client()

        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C.post(registration_url, registration_data)

        user = CustomUser.objects.get(username='testuser2')
        user.group = 'test'
        user.save()
        user.role='Owner'
        user.save()

        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser2',
            'password': 'TestPassword123!',
        }

        C.post(login_url, login_data)
        C.get(reverse('add_to_group'), {'user_email':'testuser@example.com'})

        self.client.post(reverse('manage'), {'role_response':'accept'}, follow=True)
        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'testuser2')
    
    def test_invite_decline(self):
        C = Client()

        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        C.post(registration_url, registration_data)

        user = CustomUser.objects.get(username='testuser2')
        user.group = 'test'
        user.save()
        user.role='Owner'
        user.save()

        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser2',
            'password': 'TestPassword123!',
        }

        C.post(login_url, login_data)
        C.get(reverse('add_to_group'), {'user_email':'testuser@example.com'})

        self.client.post(reverse('manage'), {'role_response':'decline'}, follow=True)
        response = self.client.get(reverse('manage'))
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'Create group')
    
    def test_create_group(self):
        response = self.client.get(reverse('new_group'), {'group_name':'test'}, follow=True)
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'test group members:')

    def test_delete_group(self):
        response = self.client.get(reverse('new_group'), {'group_name':'test'}, follow=True)
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'test group members:')
        response = self.client.get(reverse('delete_group'), follow=True)
        self.assertTemplateUsed(response, "cma/manage.html")
        self.assertContains(response, 'Create group')

class FilesViewsTest(TestCase):
    def setUp(self):
        # Set up a client for making requests
        self.client = Client()

        # Register user
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        self.client.post(registration_url, registration_data)

        #login to account
        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }

        self.client.post(login_url, login_data)

    def test_files_empty(self):
        response = self.client.get(reverse('view_all_files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/files.html")
        self.assertContains(response, 'No files have been uploaded.')
    
    def test_files_and_upload(self):
        self.dummy_file = SimpleUploadedFile("dummy.txt", b"Dummy file content.")

        fileData = {
            'switch_value':'off',
            'file': self.dummy_file,
            'fileName':'testFile'
        }

        self.client.post(reverse('upload_file'), fileData)
        response = self.client.get(reverse('view_all_files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/files.html")
        self.assertContains(response, 'testFile')
    
    def test_view_file(self):
        self.dummy_file = SimpleUploadedFile("dummy.txt", b"Dummy file content.")

        fileData = {
            'switch_value':'off',
            'file': self.dummy_file,
            'desc':'test file description',
            'fileName':'testFile'
        }

        self.client.post(reverse('upload_file'), fileData)

        file = CMDoc.objects.get(fileName='testFile')
        slug = file.slug
        response = self.client.get(f"/CMA/view/{slug}", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/view_CMDoc.html")
        self.assertContains(response, 'test file description')
    
    def test_download_file(self):
        self.dummy_file = SimpleUploadedFile("dummy.txt", b"Dummy file content.")

        fileData = {
            'switch_value':'off',
            'file': self.dummy_file,
            'desc':'test file description',
            'fileName':'testFile'
        }

        self.client.post(reverse('upload_file'), fileData)

        file = CMDoc.objects.get(fileName='testFile')
        file_id = file.pk
        response = self.client.get(f"/CMA/download/{file_id}", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn('filename="dummy.txt"', response['Content-Disposition'])
    
    def test_delete_file(self):
        self.dummy_file = SimpleUploadedFile("dummy.txt", b"Dummy file content.")

        fileData = {
            'switch_value':'off',
            'file': self.dummy_file,
            'fileName':'testFile'
        }

        self.client.post(reverse('upload_file'), fileData)
        response = self.client.get(reverse('view_all_files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/files.html")
        self.assertContains(response, 'testFile')

        file = CMDoc.objects.get(fileName='testFile')
        file_id = file.pk
        self.client.get(f"/CMA/delete/{file_id}", follow=True)

        response = self.client.get(reverse('view_all_files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/files.html")
        self.assertNotContains(response, 'testFile')

class ChatsViewsTest(TestCase):
    def setUp(self):
        # Set up a client for making requests
        self.client = Client()

        # Register user
        registration_url = reverse('register_view')
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'ToS': True,
        }

        self.client.post(registration_url, registration_data)

        #login to account
        login_url = reverse('login_view')
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }

        self.client.post(login_url, login_data)

    def test_chats_empty(self):
        response = self.client.get(reverse('view_all_chats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/chats.html")
        self.assertContains(response, 'No chats have been created.')
    
    def test_chats_and_create(self):
        chatData = {
            'chat_name':'testChat'
        }

        self.client.get(reverse('new_chat'), chatData)
        response = self.client.get(reverse('view_all_chats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/chats.html")
        self.assertContains(response, 'testChat')
    
    def test_view_chat(self):
        chatData = {
            'chat_name':'testChat'
        }

        self.client.get(reverse('new_chat'), chatData)

        chat = Chat.objects.get(chatName='testChat')
        slug = chat.slug
        response = self.client.get(f"/CMA/chat/view/{slug}", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/view_chat.html")
        self.assertContains(response, 'No chat history available.')
    
    def test_delete_chat(self):
        chatData = {
            'chat_name':'testChat'
        }

        self.client.get(reverse('new_chat'), chatData)
        response = self.client.get(reverse('view_all_chats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/chats.html")
        self.assertContains(response, 'testChat')

        chat = Chat.objects.get(chatName='testChat')
        slug = chat.slug
        self.client.get(f"/CMA/delete/{slug}", follow=True)

        response = self.client.get(reverse('view_all_chats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cma/chats.html")
        self.assertContains(response, 'testChat')
