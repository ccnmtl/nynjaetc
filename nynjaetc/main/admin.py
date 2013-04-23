from pagetree.models import Section
from django.contrib import admin
from models import Preference, SectionPreference, EncryptedUserDataField

class PreferenceAdmin (admin.ModelAdmin):
    list_display = ( 'slug',)
    fields = ('slug', )     
admin.site.register(Preference, PreferenceAdmin)


class SectionPreferenceAdmin (admin.ModelAdmin):
    list_display = ( 'section', 'preference', )
    fields =  ( 'section', 'preference', )
admin.site.register(SectionPreference, SectionPreferenceAdmin)



class EncryptedUserDataFieldAdmin (admin.ModelAdmin):
    list_display = ( 'slug',)
    fields = ('slug', )
admin.site.register(EncryptedUserDataField, EncryptedUserDataFieldAdmin)
