from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser('amir@amir.com', 'test123')
        self.client.force_login(self.admin_user)  # why force
        self.user = get_user_model().objects.create_user(email='bbbb@bbb.com', password='123gfhfjf', name='pgl')

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
