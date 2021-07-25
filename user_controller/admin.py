from django.contrib import admin
from .models import CustomUser, Jwt, UserProfile


admin.site.register((CustomUser, Jwt, ))
admin.site.register(UserProfile)
