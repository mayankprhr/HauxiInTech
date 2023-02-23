from django.urls import path
from .views import *
from .views_api import *

urlpatterns = [
    path('login/',LoginView),
    path('register/',RegisterView)
    
]
