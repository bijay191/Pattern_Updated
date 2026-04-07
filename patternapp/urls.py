from django.urls import path
from .views import generate_regex

urlpatterns = [
    path('', generate_regex, name='generate'),
]