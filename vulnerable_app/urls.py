"""
vulnerable_app/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/users/', views.user_list, name='user_list'),
    path('api/users/<int:user_id>/', views.user_by_id, name='user_by_id'),
    path('api/search/', views.search, name='search'),
    path('api/transfer/', views.transfer, name='transfer'),
    path('api/profile/', views.profile, name='profile'),
]
