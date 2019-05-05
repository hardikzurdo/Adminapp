from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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

        def test_create_token_for_user(self):
            """Test that token is created for user"""
            payload = {'email': 'tata@nano.com', 'password': 'password1234'}
            create_user(**payload)
            res = self.client.post(TOKEN_URL, payload)

            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        def test_create_token_invalid_credentials(self):
            """Test token is not created if invalid credentials are given"""
            create_user(email='tata@nano.com', password='password123')
            payload = {'email': 'tata@nano.com', 'password': 'wrongpassword'}
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_no_user(self):
            """Test for token if user is not exists"""
            payload = {'email': 'tata@nano.com', 'password': 'password1234'}
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_missing_field(self):
            """test for userenail and password are require"""
            res = self.client.post(TOKEN_URL, {'email': 'one', 'password':''})
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def Test_retrive_user_unauthorized(self):
            """ Test for Authentication is require for users"""
            res = self.client.get(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
        """Test for API requests that require authentication"""

        def setUp(self):
            self.user = create_user(
                email='tata@nano.com',
                password='password1234',
                name='ratan'
            )
            self.client = APIClient()
            self.client.force_authenticate(user=self.user)

        def test_retrive_profile_success(self):
            """Test retriving profile for loggeg in used"""
            res = self.client.get(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, {
                'name': self.user.name,
                'email': self.user.email
            })

        def test_post_me_not_allowed(self):
            """Test for POST is not allowed for the me URL"""
            res = self.client.post(ME_URL, {})

            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_update_ser_profile(self):
            """test updating the user profile for authentication user"""
            payload = {'name':'new','password':'newpassword123'}

            res = self.client.patch(ME_URL, payload)

            self.user.refresh_from_db()

            self.assertEqual(self.user.name, payload['name'])
            self.assertTrue(self.user.check_password(payload['password']))
            self.assertEqual(res.status_code, status.HTTP_200_OK)
