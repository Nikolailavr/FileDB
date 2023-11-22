from django.contrib import admin

from filedb.models import File


@admin.register(File)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['type', 'vendor', 'date_revision']
    search_fields = ['type', 'vendor', 'date_revision', 'extra_field']
    list_filter = ['type', 'vendor', 'date_revision', 'extra_field']

