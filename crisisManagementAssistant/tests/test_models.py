from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from crisisManagementAssistant.models import CMDoc, Chat

class CMDocModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'group': 'test_group',
            'role': 'test_role',
            'settings': {'key': 'value'},
        }
        self.user = get_user_model().objects.create(**self.user_data)
        self.cmdoc_data = {
            'user': self.user,
            'fileName': 'testfile',
            'desc': 'Test description',
            'file': SimpleUploadedFile("testfile.txt", b"file_content"),
            'extractData': {'key': 'value'},
        }
        self.cmdoc = CMDoc.objects.create(**self.cmdoc_data)

    def test_cmdoc_creation(self):
        self.assertEqual(self.cmdoc.user, self.user)
        self.assertEqual(self.cmdoc.fileName, 'testfile')
        self.assertEqual(self.cmdoc.desc, 'Test description')
        self.assertEqual(self.cmdoc.file.read(), b"file_content")
        self.assertEqual(self.cmdoc.extractData, {'key': 'value'})

    def test_cmdoc_unique_slug(self):
        other_cmdoc = CMDoc.objects.create(user=self.user, fileName='testfile', desc='Other description')
        self.assertNotEqual(self.cmdoc.slug, other_cmdoc.slug)

    def test_cmdoc_update(self):
        updated_data = {
            'fileName': 'updatedfile',
            'desc': 'Updated description',
            'file': SimpleUploadedFile("updatedfile.txt", b"updated_file_content"),
            'extractData': {'updated_key': 'updated_value'},
        }

        for field, value in updated_data.items():
            setattr(self.cmdoc, field, value)
        
        self.cmdoc.save()

        # Save the file separately, as updating a FileField requires specific handling
        updated_file = SimpleUploadedFile("updatedfile.txt", b"updated_file_content")
        self.cmdoc.file.save(updated_file.name, updated_file, save=False)

        self.cmdoc.save()

        updated_cmdoc = CMDoc.objects.get(pk=self.cmdoc.pk)

        for field, value in updated_data.items():
            if field == 'file':
                # Compare file content instead of the file field itself
                self.assertEqual(updated_cmdoc.file.read(), b"updated_file_content")
            else:
                self.assertEqual(getattr(updated_cmdoc, field), value)

    def test_cmdoc_deletion(self):
        cmdoc_id = self.cmdoc.id
        self.cmdoc.delete()

        with self.assertRaises(CMDoc.DoesNotExist):
            CMDoc.objects.get(pk=cmdoc_id)

    def test_cmdoc_ordering(self):
        # Add more CMDocs to test ordering
        cmdoc1 = CMDoc.objects.create(user=self.user, fileName='file1', desc='Description 1')
        cmdoc2 = CMDoc.objects.create(user=self.user, fileName='file2', desc='Description 2')

        cmdocs = CMDoc.objects.all()
        self.assertEqual(cmdocs[0], self.cmdoc)
        self.assertEqual(cmdocs[1], cmdoc1)
        self.assertEqual(cmdocs[2], cmdoc2)

    def test_cmdoc_absolute_url(self):
        expected_url = reverse("view_file", kwargs={"slug": self.cmdoc.slug})
        self.assertEqual(self.cmdoc.get_absolute_url(), expected_url)

    def test_cmdoc_download_url(self):
        expected_url = reverse("download_file", kwargs={"file_id": self.cmdoc.id})
        self.assertEqual(self.cmdoc.get_download_url(), expected_url)

    def test_cmdoc_delete_url(self):
        expected_url = reverse("delete_file", kwargs={"file_id": self.cmdoc.id})
        self.assertEqual(self.cmdoc.get_delete_url(), expected_url)


class ChatModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', email='testuser@example.com')
        self.chat_data = {
            'user': self.user,
            'chatName': 'testchat',
            'chatData': {'key': 'value'},
        }
        self.chat = Chat.objects.create(**self.chat_data)

    def test_chat_creation(self):
        self.assertEqual(self.chat.user, self.user)
        self.assertEqual(self.chat.chatName, 'testchat')
        self.assertEqual(self.chat.chatData, {'key': 'value'})

    def test_chat_unique_slug(self):
        other_chat = Chat.objects.create(user=self.user, chatName='testchat', chatData={'other_key': 'other_value'})
        self.assertNotEqual(self.chat.slug, other_chat.slug)

    def test_chat_update(self):
        updated_data = {
            'chatName': 'updatedchat',
            'chatData': {'updated_key': 'updated_value'},
        }

        for field, value in updated_data.items():
            setattr(self.chat, field, value)

        self.chat.save()

        updated_chat = Chat.objects.get(pk=self.chat.pk)

        for field, value in updated_data.items():
            self.assertEqual(getattr(updated_chat, field), value)

    def test_chat_deletion(self):
        chat_slug = self.chat.slug
        self.chat.delete()

        with self.assertRaises(Chat.DoesNotExist):
            Chat.objects.get(slug=chat_slug)

    def test_chat_ordering(self):
        # Add more Chats to test ordering
        chat1 = Chat.objects.create(user=self.user, chatName='chat1')
        chat2 = Chat.objects.create(user=self.user, chatName='chat2')

        chats = Chat.objects.all()
        self.assertEqual(chats[0], self.chat)
        self.assertEqual(chats[1], chat1)
        self.assertEqual(chats[2], chat2)
    
    def test_chat_absolute_url(self):
        expected_url = reverse("view_chat", kwargs={"slug": self.chat.slug})
        self.assertEqual(self.chat.get_absolute_url(), expected_url)

    def test_chat_delete_url(self):
        expected_url = reverse("delete_chat", kwargs={"slug": self.chat.slug})
        self.assertEqual(self.chat.get_delete_url(), expected_url)

    def test_chat_regen_context_url(self):
        expected_url = reverse("regen_context_chat", kwargs={"slug": self.chat.slug})
        self.assertEqual(self.chat.get_regen_context_url(), expected_url)
