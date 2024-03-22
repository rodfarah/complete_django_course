from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'recipes/category/<int:category_id>/', views.category,
        name='category'),
    path('recipes/<int:one_id>/', views.one_recipe, name='one_recipe'),]
