from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, EffortAuthenticate, OtpCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    readonly_fields = ('last_login', )

    fieldsets = (
        (None, {"fields": ('username', 'email', 'phone_number', 'password')}),
        ('Permissions', {"fields": ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {"fields": ('username', 'email', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            field = form.base_fields.get('is_superuser')
            if field:
                field.disabled = True
        return form


admin.site.register(User, UserAdmin)
admin.site.register(EffortAuthenticate)
admin.site.register(OtpCode)
