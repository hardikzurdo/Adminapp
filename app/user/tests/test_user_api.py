from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users(Public users)"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creaing user with valid payload is successfull"""
        payload = {
            'email': 'tata@nano.com',
            'password': 'tatanano123',
            'name': 'Ratan Tata'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        def test_user_exists(self):
            """Test creating user that already exists fails"""
            payload = {'email': 'tata@nanonano.com', 'password': 'nanonano'}
            create_user(**payload)

            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def password_too_short(self):
            """Test for password which must be more then 8 char long"""
            payload = {'email': 'jamshed@tata.com', 'password': 'pwd'}
            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.staus_code, status.HTTP_400_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
            self.assertFalse(user_exists)
