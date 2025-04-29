from django.contrib import admin
from .models import University, ServiceAccount

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display  = ['code', 'name', 'specialist_email']
    search_fields = ['code', 'name']

@admin.register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    list_display   = ['name', 'university', 'token']
    raw_id_fields  = ['token']
    autocomplete_fields = ['university']
