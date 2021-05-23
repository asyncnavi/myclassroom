from django.contrib import admin
from .models import User
from .forms import AdminUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = AdminUserCreationForm
    fieldsets = (
        (
            "User Info",
            {
                'fields': ('name',
                           'profile_image',
                           'date_of_birth',
                           'mobile', 'bio')
            }
        ),
        *UserAdmin.fieldsets,

    )


admin.site.register(User, CustomUserAdmin)
