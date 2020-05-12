from django.contrib import admin
from .models import (
    SampleInfo, AnimalInfo, SampleDataInfo, Species2CommonName, DADISLink)


class Species2CommonNameAdmin(admin.ModelAdmin):
    list_display = ('scientific_name', 'common_name')


class DADISLinkAdmin(admin.ModelAdmin):
    list_display = (
        'species', 'supplied_breed', 'efabis_breed_country', 'dadis_url'
    )


admin.site.register(SampleInfo)
admin.site.register(AnimalInfo)
admin.site.register(SampleDataInfo)
admin.site.register(Species2CommonName, Species2CommonNameAdmin)
admin.site.register(DADISLink, DADISLinkAdmin)
