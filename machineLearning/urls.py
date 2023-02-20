from django.urls import path
from .views import *

urlpatterns = [
    path('', capture_frames, name='machine-learning'),
]
