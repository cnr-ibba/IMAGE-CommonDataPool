from django.contrib import admin
from .models import SampleInfo, AnimalInfo, SampleDataInfo

admin.site.register(SampleInfo)
admin.site.register(AnimalInfo)
admin.site.register(SampleDataInfo)
