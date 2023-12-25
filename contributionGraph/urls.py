# pages/urls.py
from django.urls import path
from . views import home, github_contributions

urlpatterns = [
    path('', home, name='home'),
    path('load/', github_contributions, name='graph'),
]
