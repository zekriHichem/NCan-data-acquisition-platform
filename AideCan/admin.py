from django.contrib import admin

from AideCan.models import *
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Mammography)
admin.site.register(Diagnostic)
admin.site.register(ModelVersion)
