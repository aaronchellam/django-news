from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Specify the form to be used for user creation in the admin interface.
    add_form = CustomUserCreationForm

    # Specify the form to be used for user changes in the admin interface.
    form = CustomUserChangeForm

    # Specify the model that this admin class is associated with.
    model = CustomUser

    # Custmise the list display columns in the admin user list view.
    list_display = [
        "email",
        "username",
        "age",
        "is_staff",
    ]

    # Extend the fieldsets from the base UserAdmin class with an additional field 'age'.
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),)

    # Extend the add_fieldsets from the base UserAdmin class with an additional field 'age'.
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)


admin.site.register(CustomUser, CustomUserAdmin)