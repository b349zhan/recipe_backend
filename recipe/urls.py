from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import recipe_names, recipe_detail

urlpatterns = [
    path('', recipe_names),
    path('details/<recipe_name>', recipe_detail)
]