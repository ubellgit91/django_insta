from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import User
from .forms import SignupForm

# Register your models here.
user = get_user_model()

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가정보', {'fields': ('img_profile', 'gender')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('img_profile', 'gender',),
        }),
    )
    add_form = SignupForm


# ModelAdmin은 패키지에 정의되어있는 UserAdmin을 import해와서 쓴다.
admin.site.register(User, UserAdmin)