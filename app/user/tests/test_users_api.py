from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {'email': 'test@phl.com',
                   'password': 'mypassword12%^',
                   'name': 'pooya phl'}

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)  # todo read other codes
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data.keys())

    def test_user_exists(self):
        payload = {'email': 'test@phl.com',
                   'password': 'mypassword12%^',
                   'name': 'pooya phl'}

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('password', res.data.keys())

    def test_password_too_short(self):
        """more than 5"""
        payload = {'email': 'test@phl.com',
                   'password': 'my%^',
                   'name': 'pooya phl'}

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertNotIn('password', res.data.keys())
        exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(exists)
