from django.contrib import admin
from models import Preference, SectionPreference


class PreferenceAdmin (admin.ModelAdmin):
    list_display = ('slug',)
    fields = ('slug', )
admin.site.register(Preference, PreferenceAdmin)


class SectionPreferenceAdmin (admin.ModelAdmin):
    list_display = ('section', 'preference', )
    fields = ('section', 'preference', )
admin.site.register(SectionPreference, SectionPreferenceAdmin)
