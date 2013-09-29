from django.contrib import admin
from restAPI.models import Station

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Make the restAPI models accessible in the django admin console
admin.site.register(User)
admin.site.register(Station)
