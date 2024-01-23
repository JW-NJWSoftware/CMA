from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import get_user_model

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'group': 'test_group',
            'role': 'test_role',
            'settings': {'key': 'value'},
        }
        self.user = get_user_model().objects.create(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.group, 'test_group')
        self.assertEqual(self.user.role, 'test_role')
        self.assertEqual(self.user.settings, {'key': 'value'})

    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_update(self):
        updated_data = {
            'username': 'updateduser',
            'group': 'updated_group',
            'role': 'updated_role',
            'settings': {'updated_key': 'updated_value'},
        }

        for field, value in updated_data.items():
            setattr(self.user, field, value)

        self.user.save()

        updated_user = get_user_model().objects.get(pk=self.user.pk)

        for field, value in updated_data.items():
            self.assertEqual(getattr(updated_user, field), value)

    def test_user_deletion(self):
        user_id = self.user.id
        self.user.delete()

        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=user_id)
    
    def test_user_ordering(self):
        # Add more users to test ordering
        user1 = get_user_model().objects.create(username='user1', email='user1@example.com')
        user2 = get_user_model().objects.create(username='user2', email='user2@example.com')

        users = get_user_model().objects.all()
        self.assertEqual(users[0], self.user)
        self.assertEqual(users[1], user1)
        self.assertEqual(users[2], user2)
    
    def test_unique_username(self):
        # Attempt to create another user with the same username
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create(username='testuser', email='anotheruser@example.com')

    def test_unique_email(self):
        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create(username='anotheruser', email='testuser@example.com')