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


def get_general_payload():
    return {'email': 'test@phl.com',
            'password': 'mypassword12%^',
            'name': 'pooya phl'}


class PublicUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.general_payload = get_general_payload()

    def test_create_valid_user_success(self):
        payload = self.general_payload

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)  # todo read other codes
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data.keys())

    def test_user_exists(self):
        payload = self.general_payload

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('password', res.data.keys())

    def test_password_too_short(self):
        """more than 5"""
        payload = self.general_payload
        payload['password'] = 'xy'

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertNotIn('password', res.data.keys())
        exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(exists)

    def test_create_token_for_user(self):
        payload = self.general_payload
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data.keys())  # trust token works because it is built in django auth system which
        # has it's own tests
        self.assertNotIn('password', res.data.keys())

    def test_create_token_invalid_credentials(self):
        general_payload = self.general_payload
        create_user(**general_payload)
        payload = {'email': general_payload['email'], 'password': 'wrong_pass_123$%^ha',
                   'name': general_payload['name']}

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data.keys())
        self.assertNotIn('password', res.data.keys())

    def test_create_token_no_user(self):
        payload = {'email': 'x@y.com', 'password': '123$%^ha', 'name': 'jajaja'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data.keys())
        self.assertNotIn('password', res.data.keys())

    def test_create_token_missing_field(self):
        payload = {'email': '1', 'password': '', }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data.keys())
        # self.assertNotIn('password', res.data.keys())
        # print(res.data['password'])

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    def setUp(self):
        self.user = create_user(email='abc@xyz.com', password='password1234%^&*', name='amirphl')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, {'email': self.user.email, 'name': self.user.name})

    def test_post_not_allowed(self):
        """on the ME url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'name': 'new_name', 'password': 'new_password_%^&*'}
        res = self.client.patch(ME_URL, payload)  # todo what is patch
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
