from django.urls import path, include
from rest_framework.routers import DefaultRouter  # todo read more

from recipe import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
app_name = 'recipe'
urlpatterns = [
    path('', include(router.urls))
]
