from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # Authentication
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # User Registration
    # path('register/', RegisterUser.as_view(), name='register'),

    # Gym Members
    path('members/', list_gym_members.as_view(), name='list_gym_members'),
    path('members/<int:pk>/', get_gym_member.as_view(), name='member-detail'),
    path('members/create/', create_gym_member.as_view(), name='member-create'),
    path('members/update/<int:pk>/', update_gym_member.as_view(), name='member-update'),
    path('members/delete/<int:pk>/', delete_gym_member.as_view(), name='member-delete'),
]
