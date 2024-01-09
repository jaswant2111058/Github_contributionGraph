# pages/urls.py
from django.urls import path
from . views import home, github_contributions,github_data

urlpatterns = [
    path('', home, name='home'),
    path('load/', github_contributions, name='graph'),
    path('data/', github_data, name='githubdata'),
    
]
