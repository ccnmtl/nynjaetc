from django.contrib import admin
from nynjaetc.treatment_activity.models import TreatmentNode, TreatmentPath
from treebeard.admin import TreeAdmin

admin.site.register(TreatmentNode, TreeAdmin)
admin.site.register(TreatmentPath)
