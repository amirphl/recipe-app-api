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
        # serializer = RecipeSerializer(recipes, many=True)
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

    def test_create_basic_recipe(self):
        payload = {
            'title': 'ddd',
            'time_minutes': 30,
            'price': 5.00
        }

        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(getattr(recipe, key), payload[key])

    def test_create_recipe_with_tags(self):
        tag1 = sample_tag(self.user)
        tag2 = sample_tag(self.user)
        tag3 = sample_tag(self.user)

        payload = {
            'title': 'ddd',
            'tags': [tag1.id, tag2.id, tag3.id, ],
            'time_minutes': 30,
            'price': '5.00'
        }

        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 3)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
        self.assertIn(tag3, tags)

    def test_create_ingredient_with_tags(self):
        ingredient1 = sample_ingredient(self.user)
        ingredient2 = sample_ingredient(self.user)
        ingredient3 = sample_ingredient(self.user)

        payload = {
            'title': 'ddd',
            'ingredients': [ingredient1.id, ingredient2.id, ingredient3.id, ],
            'time_minutes': 30,
            'price': '5.00'
        }

        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 3)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
        self.assertIn(ingredient3, ingredients)
