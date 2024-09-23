from django.contrib import admin

from api.models import Excerpt


class ExcerptAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('composer', 'title',)}

admin.site.register(Excerpt, ExcerptAdmin)
