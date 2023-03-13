from django.contrib import admin
from . import models


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('email', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
    )
    
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(models.CustomUser, CustomUserAdmin)