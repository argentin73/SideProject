from django.urls import re_path, path, include
from service.views import frontend

# Catch all pattern
urlpatterns = [
    path('api/', include('service.api.urls')),
    path('', frontend, name="index"),
    re_path('.*/', frontend, name="frontend")
]