from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user(self):
        """test User with email address and password"""
        email = 'testemailtest@gnail.com'
        password = 'Testpassss1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ test for email for exampt the uper lower cases"""
        email = 'testaa@GNAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test users has email ID"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating superuser ans staff permission"""
        user = get_user_model().objects.create_superuser(
            'tatanano@nano.com',
            'password1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
