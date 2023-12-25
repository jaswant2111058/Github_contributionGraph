# mysite/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contributionGraph.urls')),
    path('graph/', include('contributionGraph.urls')),
]
