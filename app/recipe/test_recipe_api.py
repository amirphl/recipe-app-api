from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id, ])


def sample_tag(user, name='tyoui'):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='tydfghoui'):
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    defaults = {'title': 'ssmmmaa', 'time_minutes': 10, 'price': 4.99}
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesAPITest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='aaa@fff.com', password='eeee%^&')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes_list(self):
        sample_recipe(self.user)
        sample_recipe(self.user)
        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        new_user = get_user_model().objects.create_user(email='new_user@new_mail.com', password='dsfndklvn')
        sample_recipe(self.user)
        sample_recipe(self.user)
        sample_recipe(new_user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        # self.assertListEqual(res.data, serializer.data) todo fix it as soon

    # def test_create_ingredient_successful(self):
    #     payload = {'name': 'fhfhfhfh'}
    #     self.client.post(INGREDIENTS_URL, payload)
    #     exists = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()
    #     self.assertTrue(exists)
    #
    # def test_create_ingredient_invalid(self):
    #     payload = {'name': ''}
    #     res = self.client.post(INGREDIENTS_URL, payload)
    #     exists = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()
    #     self.assertFalse(exists)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_recipe_detail(self):
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user))
        recipe.tags.add(sample_tag(self.user, name='rty'))
        recipe.ingredients.add(sample_ingredient(self.user))
        recipe.ingredients.add(sample_ingredient(self.user, name='ff'))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
