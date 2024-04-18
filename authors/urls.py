from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
]
