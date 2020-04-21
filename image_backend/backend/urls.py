from django.urls import path

from . import views

app_name = 'backend'


species2commonnames_list = views.SpeciesToCommonNameViewSet.as_view({
    'get': 'list'
})


urlpatterns = [
    path('organism/', views.ListOrganismsView.as_view(),
         name='organismindex'),
    path('organism_short/', views.ListOrganismsViewShort.as_view(),
         name='organismindex_short'),
    path('organism/summary/', views.get_organisms_summary,
         name='organism_summary'),
    path('organism/graphical_summary/', views.get_organisms_graphical_summary,
         name='organism_graphical_summary'),
    path('organism/gis_search/', views.organisms_gis_search,
         name='organism_gis_search'),
    path('organism/download/', views.download_organism_data,
         name='organism_download'),
    path('organism/<data_source_id>/', views.OrganismsDetailsView.as_view(),
         name='organismdetail'),
    path('specimen/', views.ListSpecimensView.as_view(),
         name='specimenindex'),
    path('specimen_short/', views.ListSpecimensViewShort.as_view(),
         name='specimenindex_short'),
    path('specimen/summary/', views.get_specimens_summary,
         name='specimen_summary'),
    path('specimen/graphical_summary/', views.get_specimens_graphical_summary,
         name='specimens_graphical_summary'),
    path('specimen/gis_search/', views.specimens_gis_search,
         name='specimen_gis_search'),
    path('specimen/download/', views.download_specimen_data,
         name='specimen_download'),
    path('specimen/<data_source_id>/', views.SpecimensDetailsView.as_view(),
         name='specimendetail'),
    path('file/', views.ListCreateFilesView.as_view(), name='fileindex'),
    path('file/download/', views.download_file_data, name='file_download'),
    path('file/<specimen_id>/', views.FilesDetailsView.as_view(),
         name='filedetail'),
    path('species', species2commonnames_list, name='species'),
]
