from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Diagnosis)
admin.site.register(Reception)
admin.site.register(PurposeOfVisit)
