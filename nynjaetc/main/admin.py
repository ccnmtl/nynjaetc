from django.contrib import admin
from models import Preference, SectionPreference, SectionAlternateNavigation


class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    fields = ('slug', )
admin.site.register(Preference, PreferenceAdmin)


class SectionPreferenceAdmin(admin.ModelAdmin):
    list_display = ('section', 'preference', )
    fields = ('section', 'preference', )
admin.site.register(SectionPreference, SectionPreferenceAdmin)


class SectionAlternateNavigationAdmin(admin.ModelAdmin):
    list_display = ('section', 'alternate_back', 'alternate_next')
    fields = ('section', 'alternate_back', 'alternate_back_label',
              'alternate_next', 'alternate_next_label',)
admin.site.register(SectionAlternateNavigation,
                    SectionAlternateNavigationAdmin)
