from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Posts, Likes, Follow

admin.site.register(User, UserAdmin)
admin.site.register(Profile)

# Register your models here.
