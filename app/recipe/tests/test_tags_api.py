from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='aaa@fff.com', password='eeee%^&')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='sssss')
        Tag.objects.create(user=self.user, name='ddddd')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        new_user = get_user_model().objects.create_user(email='new_user@new_mail.com', password='dsfndklvn')
        tag = Tag.objects.create(user=self.user, name='ddd')
        t1 = Tag.objects.create(user=new_user, name='eee')
        t2 = Tag.objects.create(user=new_user, name='ddd')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertNotEqual(res.data[0]['name'], t1.name)
        # self.assertNotEqual(res.data[0]['email'], t2.user.email) todo

    def test_create_tag_successful(self):
        payload = {'name': 'fhfhfhfh'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(user=self.user, name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(user=self.user, name=payload['name']).exists()
        self.assertFalse(exists)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
