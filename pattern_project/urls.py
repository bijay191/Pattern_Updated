from django.urls import path, include

urlpatterns = [
    path('', include('patternapp.urls')),
]