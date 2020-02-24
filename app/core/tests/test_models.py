from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@xxx.com'
        password = 'test123@#%'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_new_user_email_normalized(self):
        email = 'test@XXXCCCUUU.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123test@#')
            get_user_model().objects.create_user('', '123test@#')
            get_user_model().objects.create_user(' ', '123test@#')
            get_user_model().objects.create_user(' aa ', '123test@#')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser('aaa@gmail.com', '123test@#')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
