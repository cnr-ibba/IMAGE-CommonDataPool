from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('organism/', views.ListCreateOrganismsView.as_view(),
         name='organismindex'),
    path('organism_short/', views.ListCreateOrganismsViewShort.as_view(),
         name='organismindex_short'),
    path('organism/summary/', views.get_organisms_summary,
         name='organism_summary'),
    path('organism/graphical_summary/', views.get_organisms_graphical_summary,
         name='organism_graphical_summary'),
    path('organism/gis_search/', views.organisms_gis_search,
         name='organism_gis_search'),
    path('organism/download/', views.download_organism_data,
         name='organism_download'),
    path('organism/<organism_id>/', views.OrganismsDetailsView.as_view(),
         name='organismdetail'),
    path('specimen/', views.ListCreateSpecimensView.as_view(),
         name='specimenindex'),
    path('specimen_short/', views.ListCreateSpecimensViewShort.as_view(),
         name='specimenindex_short'),
    path('specimen/summary/', views.get_specimens_summary,
         name='specimen_summary'),
    path('specimen/graphical_summary/', views.get_specimens_graphical_summary,
         name='specimens_graphical_summary'),
    path('specimen/gis_search/', views.specimens_gis_search,
         name='specimen_gis_search'),
    path('specimen/download/', views.download_specimen_data,
         name='specimen_download'),
    path('specimen/<specimen_id>/', views.SpecimensDetailsView.as_view(),
         name='specimendetail')
]
