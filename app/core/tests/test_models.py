from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='abc@xyz.com', password='pass@#$$1567'):
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        tag = models.Tag.objects.create(user=sample_user(), name='xxxx')
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingre = models.Ingredient.objects.create(user=sample_user(), name='dddd')
        self.assertEqual(str(ingre), ingre.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(user=sample_user(), title='a', time_minutes=5, price=5.00)
        self.assertEqual(str(recipe), recipe.title)
