from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
# from rest_framework import views

urlpatterns = [
    # Authentication
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # User Registration
    # path('register/', RegisterUser.as_view(), name='register'),

    # Gym Members
    path('members/', list_gym_members, name='list_gym_members'),
    path('members/<int:pk>/', get_gym_member, name='get-member'),
    path('members/<str:username>/', get_gym_member, name='get-member'),
    path('members/create/', create_gym_member, name='member-create'),
    path('members/update/<int:pk>/', update_gym_member, name='member-update'),
    path('members/delete/<int:pk>/', delete_gym_member, name='member-delete'),
    path('login/', login_view, name='login'),

    # Add GYM
    path('GYM/', list_gym, name='list_gym'),
    path('GYM/<int:pk>/', get_gym, name='GYM-detail'),
    path('GYM/create/', create_gym, name='GYM-create'),
    path('GYM/update/<int:pk>/', update_gym, name='GYM-update'),
    path('GYM/delete/<int:pk>/', delete_gym, name='GYM-delete'),
]
